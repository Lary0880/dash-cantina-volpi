const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const zlib = require('zlib');

const RAW_HTML_PATH = 'C:\\Users\\NTI\\Documents\\VENDAS\\Relatorio_Vendas_Cantina.html';
const USERS_JSON_PATH = 'C:\\Users\\NTI\\Documents\\VENDAS\\scripts\\usuarios_acesso.json';
const OUTPUT_INDEX_PATH = 'C:\\Users\\NTI\\Documents\\VENDAS\\index.html';

function main() {
  if (!fs.existsSync(RAW_HTML_PATH)) {
    console.error('Arquivo base nao encontrado:', RAW_HTML_PATH);
    process.exit(1);
  }
  if (!fs.existsSync(USERS_JSON_PATH)) {
    console.error('Arquivo de usuarios nao encontrado:', USERS_JSON_PATH);
    process.exit(1);
  }

  let rawHtml = fs.readFileSync(RAW_HTML_PATH, 'utf8');
  const users = JSON.parse(fs.readFileSync(USERS_JSON_PATH, 'utf8'));

  // Extract the embedded base64 logo from the dashboard HTML so the login card uses the exact same brand logo
  let logoDataUri = '';
  const logoMatch = rawHtml.match(/<img\s+class="brand-logo"\s+src="(data:image\/png;base64,[^"]+)"/);
  if (logoMatch) {
    logoDataUri = logoMatch[1];
  }

  // Inject the logged-in user badge + Logout button script into the raw HTML before encrypting
  const sessionWidgetScript = `
  <script>
    (function() {
      try {
        var u = window.__VOLPI_ACTIVE_USER__;
        if (!u) {
          var saved = sessionStorage.getItem('volpi_dash_session_v1');
          if (saved) u = JSON.parse(saved);
        }
        var headerInner = document.querySelector('.header-inner');
        if (headerInner && u) {
          var userBox = document.createElement('div');
          userBox.style.cssText = 'display:inline-flex;align-items:center;gap:10px;background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.24);padding:6px 12px;border-radius:999px;color:#fff;font-size:0.78rem;font-weight:700;';
          userBox.innerHTML = '<span>👤 ' + (u.name || u.username) + '</span>' +
            '<button id="volpiLogoutBtn" type="button" style="background:#c92535;color:#fff;border:none;border-radius:999px;padding:4px 10px;font-size:0.72rem;font-weight:800;cursor:pointer;font-family:inherit;letter-spacing:0.03em;transition:opacity 0.15s;" onmouseover="this.style.opacity=0.88" onmouseout="this.style.opacity=1">🔒 Sair</button>';
          headerInner.appendChild(userBox);
          var btn = document.getElementById('volpiLogoutBtn');
          if (btn) {
            btn.addEventListener('click', function() {
              sessionStorage.removeItem('volpi_dash_session_v1');
              window.location.reload();
            });
          }
        }
      } catch (e) {}
    })();
  </script>
</body>`;

  rawHtml = rawHtml.replace('</body>', sessionWidgetScript);

  // 1. Compress the raw HTML with gzip
  const compressedPayload = zlib.gzipSync(Buffer.from(rawHtml, 'utf8'), { level: 9 });

  // 2. Generate random 256-bit Master Key and 96-bit IV for the dashboard payload
  const masterKey = crypto.randomBytes(32);
  const payloadIv = crypto.randomBytes(12);

  const payloadCipher = crypto.createCipheriv('aes-256-gcm', masterKey, payloadIv);
  const encryptedPayload = Buffer.concat([
    payloadCipher.update(compressedPayload),
    payloadCipher.final(),
    payloadCipher.getAuthTag() // 16-byte GCM auth tag at the end (WebCrypto standard)
  ]);

  // 3. Create key-wrapping envelopes for each authorized user
  const userEnvelopes = {};
  const PBKDF2_ITERATIONS = 100000;

  for (const u of users) {
    const normUser = String(u.username || '').trim().toLowerCase();
    const password = String(u.password || '');
    if (!normUser || !password) continue;

    // Hash the username so plaintext usernames aren't exposed in source code
    const userHash = crypto.createHash('sha256').update('volpi-auth-user:' + normUser).digest('hex');

    const salt = crypto.randomBytes(16);
    const wrapIv = crypto.randomBytes(12);
    const derivedKey = crypto.pbkdf2Sync(
      normUser + ':' + password,
      salt,
      PBKDF2_ITERATIONS,
      32,
      'sha256'
    );

    const userSecretData = Buffer.from(JSON.stringify({
      masterKeyB64: masterKey.toString('base64'),
      name: u.name || normUser,
      username: normUser,
      role: u.role || ''
    }), 'utf8');

    const wrapCipher = crypto.createCipheriv('aes-256-gcm', derivedKey, wrapIv);
    const wrappedCiphertext = Buffer.concat([
      wrapCipher.update(userSecretData),
      wrapCipher.final(),
      wrapCipher.getAuthTag()
    ]);

    userEnvelopes[userHash] = {
      s: salt.toString('base64'),
      iv: wrapIv.toString('base64'),
      ct: wrappedCiphertext.toString('base64'),
      it: PBKDF2_ITERATIONS
    };
  }

  const vaultBundle = {
    v: 1,
    piv: payloadIv.toString('base64'),
    pct: encryptedPayload.toString('base64'),
    users: userEnvelopes
  };

  const encryptedHtml = `<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="robots" content="noindex, nofollow" />
  <title>Acesso Restrito — Cantina Volpi · Painel de Vendas & Metas</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:ital,wght@0,500;0,600;0,700;0,800;1,600&family=Mulish:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --red-700:   #c92535;
      --red-800:   #a31c2a;
      --red-500:   #dd3545;
      --red-100:   #fbe6e8;
      --green-900: #152b16;
      --green-800: #1d3c1e;
      --green-700: #254c25;
      --green-600: #316331;
      --green-100: #e3eee3;
      --cream-50:  #fbf7ef;
      --cream-100: #f5ede0;
      --cream-200: #eadcc4;
      --cream-300: #dcc7a4;
      --gold-500:  #d89b2b;
      --ink-900:   #1f1a17;
      --ink-700:   #3a322d;
      --ink-500:   #6b5e55;
      --ink-400:   #94867b;
      --ink-200:   #ded4c4;
      --white:     #ffffff;
      --font-display: 'Hanken Grotesk', system-ui, -apple-system, sans-serif;
      --font-sans:    'Mulish', system-ui, -apple-system, sans-serif;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      min-height: 100vh;
      font-family: var(--font-sans);
      background-color: var(--cream-50);
      background-image:
        radial-gradient(circle at 15% 15%, rgba(37, 76, 37, 0.06) 0%, transparent 45%),
        radial-gradient(circle at 85% 85%, rgba(201, 37, 53, 0.06) 0%, transparent 45%);
      color: var(--ink-900);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .tricolore-top {
      height: 5px;
      width: 100%;
      background: linear-gradient(
        90deg,
        var(--green-700) 0%, var(--green-700) 33.33%,
        var(--cream-50) 33.33%, var(--cream-50) 66.66%,
        var(--red-700) 66.66%, var(--red-700) 100%
      );
    }

    .auth-wrapper {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px 16px;
    }

    .auth-card {
      width: 100%;
      max-width: 430px;
      background: var(--white);
      border: 1px solid var(--cream-200);
      border-radius: 18px;
      box-shadow: 0 20px 50px -12px rgba(31, 26, 23, 0.16), 0 4px 14px -2px rgba(31, 26, 23, 0.06);
      overflow: hidden;
    }

    .auth-header {
      background: var(--green-700);
      color: var(--cream-50);
      padding: 28px 28px 24px;
      text-align: center;
      border-bottom: 3px solid var(--red-700);
      position: relative;
    }

    .auth-logo {
      height: 54px;
      width: auto;
      object-fit: contain;
      margin-bottom: 10px;
      filter: drop-shadow(0 2px 6px rgba(0,0,0,0.2));
    }

    .auth-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.12);
      border: 1px solid rgba(255, 255, 255, 0.22);
      color: var(--cream-100);
      font-size: 0.68rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      padding: 4px 11px;
      border-radius: 999px;
      margin-bottom: 8px;
    }

    .auth-title {
      font-family: var(--font-display);
      font-size: 1.28rem;
      font-weight: 800;
      letter-spacing: -0.015em;
      color: #ffffff;
    }

    .auth-subtitle {
      font-size: 0.80rem;
      color: var(--cream-200);
      margin-top: 4px;
      font-weight: 500;
    }

    .auth-body {
      padding: 28px;
    }

    .field-group {
      margin-bottom: 18px;
    }

    .field-label {
      display: block;
      font-size: 0.72rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--ink-500);
      margin-bottom: 7px;
    }

    .input-wrap {
      position: relative;
      display: flex;
      align-items: center;
    }

    .auth-input {
      width: 100%;
      height: 46px;
      padding: 0 14px;
      font-family: var(--font-sans);
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--ink-900);
      background: var(--cream-50);
      border: 1.5px solid var(--ink-200);
      border-radius: 10px;
      transition: all 0.18s ease;
    }

    .auth-input:focus {
      outline: none;
      border-color: var(--green-700);
      background: var(--white);
      box-shadow: 0 0 0 3px rgba(37, 76, 37, 0.15);
    }

    .toggle-pass {
      position: absolute;
      right: 10px;
      background: none;
      border: none;
      color: var(--ink-500);
      cursor: pointer;
      font-size: 0.78rem;
      font-weight: 700;
      padding: 6px 8px;
      border-radius: 6px;
      font-family: var(--font-sans);
    }

    .toggle-pass:hover {
      background: var(--cream-100);
      color: var(--ink-900);
    }

    .error-msg {
      display: none;
      background: var(--red-100);
      border: 1px solid #f3b7bd;
      color: var(--red-800);
      padding: 10px 13px;
      border-radius: 10px;
      font-size: 0.80rem;
      font-weight: 700;
      margin-bottom: 16px;
      align-items: center;
      gap: 8px;
    }

    .auth-btn {
      width: 100%;
      height: 48px;
      background: var(--red-700);
      color: var(--white);
      border: none;
      border-radius: 10px;
      font-family: var(--font-display);
      font-size: 0.96rem;
      font-weight: 800;
      letter-spacing: 0.02em;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: background 0.18s ease, transform 0.1s ease;
      box-shadow: 0 4px 12px rgba(201, 37, 53, 0.25);
    }

    .auth-btn:hover {
      background: var(--red-800);
    }

    .auth-btn:active {
      transform: translateY(1px);
    }

    .auth-btn:disabled {
      opacity: 0.65;
      cursor: wait;
    }

    .auth-footer {
      padding: 14px 28px 20px;
      background: var(--cream-50);
      border-top: 1px solid var(--cream-200);
      text-align: center;
      font-size: 0.73rem;
      color: var(--ink-500);
      font-weight: 600;
    }

    .page-footer {
      text-align: center;
      padding: 14px;
      font-size: 0.74rem;
      color: var(--ink-400);
    }
  </style>
</head>
<body>
  <div class="tricolore-top"></div>

  <div class="auth-wrapper">
    <div class="auth-card">
      <div class="auth-header">
        ${logoDataUri ? `<img class="auth-logo" src="${logoDataUri}" alt="Cantina Volpi" /><br/>` : ''}
        <div class="auth-badge">🔒 Criptografia AES-256-GCM</div>
        <h1 class="auth-title">Painel de Vendas & Metas</h1>
        <p class="auth-subtitle">Acesso exclusivo para usuários autorizados</p>
      </div>

      <form id="loginForm" class="auth-body" autocomplete="on">
        <div id="errorBox" class="error-msg">
          <span>⚠️</span>
          <span id="errorText">Usuário ou senha incorretos.</span>
        </div>

        <div class="field-group">
          <label class="field-label" for="usernameInput">Usuário</label>
          <div class="input-wrap">
            <input
              id="usernameInput"
              class="auth-input"
              type="text"
              name="username"
              placeholder="Digite seu usuário"
              autocomplete="username"
              required
              autofocus
            />
          </div>
        </div>

        <div class="field-group">
          <label class="field-label" for="passwordInput">Senha</label>
          <div class="input-wrap">
            <input
              id="passwordInput"
              class="auth-input"
              type="password"
              name="password"
              placeholder="Digite sua senha"
              autocomplete="current-password"
              style="padding-right: 74px;"
              required
            />
            <button type="button" id="togglePassBtn" class="toggle-pass">Mostrar</button>
          </div>
        </div>

        <button type="submit" id="submitBtn" class="auth-btn">
          <span>Entrar no Painel</span>
          <span>➔</span>
        </button>
      </form>

      <div class="auth-footer">
        Cantina Volpi · Dados protegidos de ponta a ponta
      </div>
    </div>
  </div>

  <div class="page-footer">
    Cantina Volpi © 2026 — Dal 1992 · Cucina Italiana
  </div>

  <script>
    const VAULT = ${JSON.stringify(vaultBundle)};

    function b64ToBytes(b64) {
      const bin = atob(b64);
      const len = bin.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; i++) {
        bytes[i] = bin.charCodeAt(i);
      }
      return bytes;
    }

    async function sha256Hex(str) {
      const buf = new TextEncoder().encode(str);
      const hashBuf = await crypto.subtle.digest('SHA-256', buf);
      return Array.from(new Uint8Array(hashBuf))
        .map(b => b.toString(16).padStart(2, '0'))
        .join('');
    }

    async function gunzipBytes(compressedBytes) {
      const ds = new DecompressionStream('gzip');
      const writer = ds.writable.getWriter();
      writer.write(compressedBytes);
      writer.close();
      const response = new Response(ds.readable);
      const ab = await response.arrayBuffer();
      return new TextDecoder('utf-8').decode(ab);
    }

    async function decryptPayloadWithMasterKey(masterKeyB64, userMeta) {
      const rawMasterKey = b64ToBytes(masterKeyB64);
      const payloadIv = b64ToBytes(VAULT.piv);
      const payloadCt = b64ToBytes(VAULT.pct);

      const cryptoMasterKey = await crypto.subtle.importKey(
        'raw',
        rawMasterKey,
        { name: 'AES-GCM' },
        false,
        ['decrypt']
      );

      const compressedAb = await crypto.subtle.decrypt(
        { name: 'AES-GCM', iv: payloadIv },
        cryptoMasterKey,
        payloadCt
      );

      const decryptedHtml = await gunzipBytes(new Uint8Array(compressedAb));

      window.__VOLPI_ACTIVE_USER__ = userMeta;
      sessionStorage.setItem('volpi_dash_session_v1', JSON.stringify(userMeta));

      document.open();
      document.write(decryptedHtml);
      document.close();
    }

    // Check if there is an active unlocked session in this tab
    (async function checkSavedSession() {
      try {
        const saved = sessionStorage.getItem('volpi_dash_session_v1');
        if (!saved) return;
        const parsed = JSON.parse(saved);
        if (parsed && parsed.masterKeyB64) {
          await decryptPayloadWithMasterKey(parsed.masterKeyB64, parsed);
        }
      } catch (e) {
        sessionStorage.removeItem('volpi_dash_session_v1');
      }
    })();

    document.getElementById('togglePassBtn').addEventListener('click', function() {
      const passInput = document.getElementById('passwordInput');
      if (passInput.type === 'password') {
        passInput.type = 'text';
        this.textContent = 'Ocultar';
      } else {
        passInput.type = 'password';
        this.textContent = 'Mostrar';
      }
    });

    document.getElementById('loginForm').addEventListener('submit', async function(e) {
      e.preventDefault();
      const errBox = document.getElementById('errorBox');
      const errText = document.getElementById('errorText');
      const submitBtn = document.getElementById('submitBtn');

      errBox.style.display = 'none';
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span>Verificando credenciais...</span>';

      try {
        const normUser = document.getElementById('usernameInput').value.trim().toLowerCase();
        const password = document.getElementById('passwordInput').value;

        const userHash = await sha256Hex('volpi-auth-user:' + normUser);
        const envelope = VAULT.users[userHash];

        if (!envelope) {
          throw new Error('INVALID_CREDENTIALS');
        }

        const salt = b64ToBytes(envelope.s);
        const wrapIv = b64ToBytes(envelope.iv);
        const wrapCt = b64ToBytes(envelope.ct);

        const baseKey = await crypto.subtle.importKey(
          'raw',
          new TextEncoder().encode(normUser + ':' + password),
          'PBKDF2',
          false,
          ['deriveKey']
        );

        const wrappingKey = await crypto.subtle.deriveKey(
          {
            name: 'PBKDF2',
            salt: salt,
            iterations: envelope.it,
            hash: 'SHA-256'
          },
          baseKey,
          { name: 'AES-GCM', length: 256 },
          false,
          ['decrypt']
        );

        const unwrappedAb = await crypto.subtle.decrypt(
          { name: 'AES-GCM', iv: wrapIv },
          wrappingKey,
          wrapCt
        );

        const userSecret = JSON.parse(new TextDecoder('utf-8').decode(unwrappedAb));
        submitBtn.innerHTML = '<span>Desbloqueando painel...</span>';

        await decryptPayloadWithMasterKey(userSecret.masterKeyB64, userSecret);
      } catch (err) {
        errText.textContent = 'Usuário ou senha incorretos. Verifique seus dados e tente novamente.';
        errBox.style.display = 'flex';
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<span>Entrar no Painel</span><span>➔</span>';
      }
    });
  </script>
</body>
</html>`;

  fs.writeFileSync(OUTPUT_INDEX_PATH, encryptedHtml, 'utf8');
  console.log('Dashboard criptografado com sucesso em:', OUTPUT_INDEX_PATH);
  console.log('Usuarios habilitados:', users.map(u => u.username).join(', '));
  console.log('Tamanho original:', (rawHtml.length / 1024).toFixed(1), 'KB -> Criptografado + Compactado:', (encryptedHtml.length / 1024).toFixed(1), 'KB');
}

main();

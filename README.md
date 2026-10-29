# 🔒 Arquitetura de Dados & Segurança — Dashboard Cantina Volpi

Este repositório contém a pipeline de extração em **Python** e o motor de criptografia **Zero-Knowledge (Client-Side AES-256-GCM)** do Dashboard de Vendas e Metas da Cantina Volpi.

## 🛡️ Arquitetura de Segurança (scripts/encrypt_dashboard.js)
O arquivo index.html publicado no GitHub Pages utiliza **Envelope Encryption (Key Wrapping)** para garantir que nenhum dado financeiro, meta ou nome de usuário fique exposto em texto claro no código-fonte:

1. **Compressão & Criptografia do Payload Principal (AES-256-GCM):**
   * O HTML do painel gerado pelo Python é comprimido com gzip (nível 9).
   * A cada build, é gerada uma **Master Key aleatória de 256 bits** (crypto.randomBytes(32)) e um **IV de 96 bits** (crypto.randomBytes(12)).
   * O payload comprimido é criptografado com AES-256-GCM + AuthTag de 128 bits (16 bytes) para garantia de integridade e autenticidade (AEAD).

2. **Derivação de Chaves por Usuário (PBKDF2-HMAC-SHA256) & Key Wrapping:**
   * Os identificadores de usuário (username) nunca ficam em texto plano no VAULT: são indexados via hash SHA-256('volpi-auth-user:' + username).
   * Para cada usuário autorizado (lido localmente de usuarios_acesso.json, que **nunca** é enviado ao GitHub), é gerado um Salt criptográfico único de 128 bits (16 bytes) e um IV de 96 bits.
   * Uma chave de envelopamento (Derived Key de 256 bits) é derivada com **100.000 iterações de PBKDF2-HMAC-SHA256** sobre username:password.
   * A Master Key é cifrada com AES-256-GCM usando a chave derivada de cada usuário, permitindo **multi-usuários independentes** sem duplicar o payload criptografado.

3. **Descriptografia 100% Client-Side (Web Crypto API):**
   * No navegador, a descriptografia utiliza exclusivamente window.crypto.subtle (PBKDF2 -> AES-GCM unwrap -> AES-GCM decrypt -> DecompressionStream('gzip')).

---

## 🐍 Scripts em Python (scripts/)
* scripts/extract_vendas_e_metas.py — Extrai o faturamento diário (Turnos Dia & Noite e Delivery/DK) diretamente do XML interno das planilhas .xlsx da pasta VENDAS/ e cruza com as metas semanais.
* scripts/extract_full_semanal.py — Extrai todos os indicadores semanais e acumulados das 3 categorias (VENDAS, QUALIDADE e CUSTOS) das planilhas da pasta SEMANAL/.
* scripts/build_dashboard_v3.py — Compila os dados processados em um painel HTML interativo autocontido.
* scripts/encrypt_dashboard.js — Aplica a criptografia AES-256-GCM + PBKDF2 gerando o index.html blindado.
* scripts/publish_github_pages.py — Automatiza a criptografia e publicação via GitHub CLI API.
* Atualizar_Dashboard.py — Script orquestrador local que executa toda a pipeline em sequência.

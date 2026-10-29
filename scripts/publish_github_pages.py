import base64
import json
import os
import subprocess
import sys

GH_EXE = r"C:\Program Files\GitHub CLI\gh.exe"
REPO_NAME = "dash-cantina-volpi"
INDEX_PATH = r"C:\Users\NTI\Documents\VENDAS\index.html"
ENCRYPT_SCRIPT = r"C:\Users\NTI\Documents\VENDAS\scripts\encrypt_dashboard.js"

def run_gh(args, input_bytes=None):
    cmd = [GH_EXE] + args
    res = subprocess.run(cmd, input=input_bytes, capture_output=True)
    return res.returncode, res.stdout.decode("utf-8", errors="replace"), res.stderr.decode("utf-8", errors="replace")

def main():
    # 0. Encrypt dashboard into index.html before uploading
    if os.path.exists(ENCRYPT_SCRIPT):
        print("Criptografando painel (AES-256-GCM) com multi-acesso...")
        enc_res = subprocess.run(["node", ENCRYPT_SCRIPT], capture_output=True, text=True, encoding="utf-8", errors="replace")
        if enc_res.returncode != 0:
            print("ERRO ao criptografar o painel:", enc_res.stderr)
            sys.exit(1)
        print(enc_res.stdout.strip())

    # 1. Verify authenticated user
    code, out, err = run_gh(["api", "user"])
    if code != 0:
        print("ERRO: Voce ainda nao fez login no GitHub CLI. Execute o login primeiro.")
        print(err)
        sys.exit(1)
    user_data = json.loads(out)
    owner = user_data["login"]
    print(f"Conectado ao GitHub como: {owner}")

    # 2. Check if repository exists; if not, create it
    code, out, err = run_gh(["api", f"repos/{owner}/{REPO_NAME}"])
    if code != 0:
        print(f"Criando repositorio publico {owner}/{REPO_NAME}...")
        c2, o2, e2 = run_gh([
            "api", "--method", "POST", "user/repos",
            "-f", f"name={REPO_NAME}",
            "-f", "description=Dashboard de Metas Semanais e Vendas - Cantina Volpi",
            "-F", "private=false",
            "-F", "auto_init=true"
        ])
        if c2 != 0:
            print("Erro ao criar repositorio:", e2)
            sys.exit(1)
        print("Repositorio criado com sucesso!")

    # 3. Check if index.html already exists in repo to get its SHA
    sha = None
    code, out, err = run_gh(["api", f"repos/{owner}/{REPO_NAME}/contents/index.html"])
    if code == 0:
        try:
            sha = json.loads(out).get("sha")
        except Exception:
            sha = None

    # 4. Read index.html and encode in base64
    with open(INDEX_PATH, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode("ascii")

    payload = {
        "message": "Atualizacao do Dashboard de Vendas e Metas - Cantina Volpi",
        "content": content_b64,
        "branch": "main"
    }
    if sha:
        payload["sha"] = sha

    print("Enviando index.html para o GitHub...")
    c3, o3, e3 = run_gh(
        ["api", "--method", "PUT", f"repos/{owner}/{REPO_NAME}/contents/index.html", "--input", "-"],
        input_bytes=json.dumps(payload).encode("utf-8")
    )
    if c3 != 0:
        print("Erro ao enviar index.html:", e3)
        sys.exit(1)
    print("Arquivo index.html publicado com sucesso!")

    # 5. Ensure GitHub Pages is enabled on main branch
    pages_payload = {
        "source": {
            "branch": "main",
            "path": "/"
        }
    }
    run_gh(
        ["api", "--method", "POST", f"repos/{owner}/{REPO_NAME}/pages", "--input", "-"],
        input_bytes=json.dumps(pages_payload).encode("utf-8")
    )

    pages_url = f"https://{owner}.github.io/{REPO_NAME}/"
    print("\n" + "=" * 68)
    print(f"DASHBOARD ONLINE NO GITHUB PAGES: {pages_url}")
    print("=" * 68)

if __name__ == "__main__":
    main()

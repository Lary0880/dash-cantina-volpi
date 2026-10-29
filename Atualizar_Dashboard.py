import subprocess, sys, os, shutil

scripts_dir = r'C:\Users\NTI\Documents\VENDAS\scripts'
s1 = os.path.join(scripts_dir, 'extract_vendas_e_metas.py')
s2 = os.path.join(scripts_dir, 'extract_full_semanal.py')
s3 = os.path.join(scripts_dir, 'build_dashboard_v3.py')

print("1/3 Lendo planilhas de VENDAS (Dia & Noite)...")
subprocess.run([sys.executable, s1], check=True)

print("2/3 Lendo planilhas SEMANAL (Vendas, Qualidade e Custos)...")
subprocess.run([sys.executable, s2], check=True)

print("3/3 Gerando paineis HTML atualizados...")
subprocess.run([sys.executable, s3], check=True)

obsidian_copy = r'G:\Meu Drive\Lalissa\Lalissa\_Anexos\Relatorio_Vendas_Cantina.html'
if os.path.exists(os.path.dirname(obsidian_copy)):
    shutil.copyfile(r'C:\Users\NTI\Documents\VENDAS\Relatorio_Vendas_Cantina.html', obsidian_copy)
    print("Copia do Obsidian sincronizada em:", obsidian_copy)

print("\nDashboard atualizado com sucesso!")

import os
import subprocess
import numpy as np
import platform

tamanhos = range(10000, 100001, 10000)
num_execucoes = 50

# Ajusta os comandos para o sistema operacional atual
is_windows = platform.system() == "Windows"
c_exec_rel_path = os.path.join("grupo16_BuscaAutoOrganizavel", "codigo", "c", "busca_c_exec.exe" if is_windows else "busca_c_exec")
c_exec_path = os.path.abspath(c_exec_rel_path)

# Dicionário de comandos (ajuste os comandos de compilação/execução)
comandos = {
    "C": {
        "compilar": f"gcc -D_POSIX_C_SOURCE=200809L {os.path.join('grupo16_BuscaAutoOrganizavel', 'codigo', 'c', 'busca_c.c')} -o {c_exec_path} -O2 -lpthread", # Adicionado -D_POSIX_C_SOURCE
        "executar": c_exec_path
    },
    "Java": {
        # Compilar Java pode ser feito uma vez antes do loop
        "compilar": f"javac -d {os.path.join('grupo16_BuscaAutoOrganizavel', 'codigo', 'java', 'out')} {os.path.join('grupo16_BuscaAutoOrganizavel', 'codigo', 'java', 'BuscaJava.java')}",
        "executar": f"java -cp {os.path.join('grupo16_BuscaAutoOrganizavel', 'codigo', 'java', 'out')} BuscaJava"
    },
    "Python": {
        "compilar": None, # Não precisa compilar
        "executar": f"python {os.path.join('grupo16_BuscaAutoOrganizavel', 'codigo', 'python', 'busca_py.py')}"
    }
}

# Criar pasta de estatísticas [cite: 49]
os.makedirs("resultados/estatisticas", exist_ok=True)

for lang, cmds in comandos.items():
    print(f"--- Executando para {lang} ---")

    # Compilar (se necessário)
    if cmds["compilar"]:
        print("Compilando...")
        try:
            subprocess.run(cmds["compilar"], shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erro na compilação: {e}")
            continue

    # Caminho do arquivo de resultados 
    path_resultados = f"resultados/estatisticas/resultados_{lang}.csv"

    with open(path_resultados, 'w') as f_out:
        # Cabeçalho do CSV [cite: 96]
        f_out.write("n,tempo_ms,desvio\n") 

        for n in tamanhos:
            print(f"Testando n={n}...")
            tempos_ms = []

            for i in range(1, num_execucoes + 1):
                # Caminho do arquivo de dados [cite: 74, 75]
                arquivo_csv_relativo = f"dados/n{n:06d}/run_{i:03d}.csv"
                arquivo_csv_abs = os.path.abspath(arquivo_csv_relativo)
                # Executa e captura a saída (o tempo em ms)
                cmd_completo = f"{cmds['executar']} {arquivo_csv_abs}"
                try:
                    resultado = subprocess.run(cmd_completo, shell=True, capture_output=True, text=True, check=True)
                    tempo = float(resultado.stdout.strip())
                    tempos_ms.append(tempo)
                except (subprocess.CalledProcessError, ValueError) as e:
                    print(f"Erro na execução: {e}")
                    continue

            # Calcular média e desvio padrão 
            media = np.mean(tempos_ms)
            desvio = np.std(tempos_ms)

            # Escrever no arquivo 
            f_out.write(f"{n},{media},{desvio}\n")

print("Execução dos experimentos concluída.")
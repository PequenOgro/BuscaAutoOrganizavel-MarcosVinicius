import os
import subprocess
import numpy as np
import platform
import sys

# Define o nome da pasta base do projeto
base_dir = "grupo16_BuscaAutoOrganizavel"

# --- Configurações do Experimento ---
tamanhos = range(10000, 100001, 10000)
num_execucoes = 50

# Detectar o sistema operacional para ajustar os comandos
is_windows = platform.system() == "Windows"
exe_suffix = ".exe" if is_windows else ""
path_sep = os.path.sep # / ou \

# --- Dicionário de Comandos ---
# Constrói os caminhos usando os.path.join para ser seguro
# Assumindo que este script (executar_experimentos.py) está na pasta RAIZ (ex: Aed2/)
# E 'grupo16_BuscaAutoOrganizavel' está DENTRO da pasta raiz.

comandos = {
    "C": {
        "compilar": f"gcc {os.path.join(base_dir, 'codigo', 'c', 'busca_c.c')} -o {os.path.join(base_dir, 'codigo', 'c', 'busca_c_exec' + exe_suffix)}",
        "executar": f"{os.path.join(base_dir, 'codigo', 'c', 'busca_c_exec' + exe_suffix)}"
    },
    "Java": {
        "compilar": f"javac -d {os.path.join(base_dir, 'codigo', 'java')} {os.path.join(base_dir, 'codigo', 'java', 'BuscaJava.java')}",
        "executar": f"java -cp {os.path.join(base_dir, 'codigo', 'java')} BuscaJava"
    },
    "Python": {
        "compilar": None, # Não precisa compilar
        "executar": f"{sys.executable} {os.path.join(base_dir, 'codigo', 'python', 'busca_py.py')}"
    }
}

# Criar pasta de estatísticas
stats_dir = os.path.join(base_dir, "resultados", "estatisticas")
os.makedirs(stats_dir, exist_ok=True)

# --- Loop Principal de Execução ---
for lang, cmds in comandos.items():
    print(f"--- Executando para {lang} ---")
    
    # Compilar (se necessário)
    if cmds["compilar"]:
        print("Compilando...")
        try:
            subprocess.run(cmds["compilar"], shell=True, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Erro de compilação para {lang}: {e.stderr}")
            continue # Pula para a próxima linguagem
            
    # Caminho do arquivo de resultados
    path_resultados = os.path.join(stats_dir, f"resultados_{lang}.csv")
    
    try:
        with open(path_resultados, 'w') as f_out:
            # Cabeçalho do CSV
            f_out.write("n,tempo_ms,desvio\n") 
            
            for n in tamanhos:
                print(f"Testando n={n}...")
                tempos_ms = []
                
                for i in range(1, num_execucoes + 1):
                    # Caminho do arquivo de dados (CORRIGIDO)
                    # Agora o caminho é relativo à pasta base
                    arquivo_csv = os.path.join(base_dir, f"dados/n{n:06d}", f"run_{i:03d}.csv") 
                    
                    # Adiciona aspas ao redor do caminho do CSV para segurança
                    # (lida com espaços em nomes de pasta, como 'Users\HP\Documents')
                    cmd_completo = f"{cmds['executar']} \"{arquivo_csv}\""
                    
                    try:
                        # Executa e captura a saída (o tempo em ms)
                        resultado = subprocess.run(cmd_completo, shell=True, capture_output=True, text=True, check=True)
                        tempo = float(resultado.stdout.strip())
                        tempos_ms.append(tempo)
                        
                    except subprocess.CalledProcessError as e:
                        print(f"Erro na execução (n={n}, run={i}, cmd={cmd_completo}): {e}")
                        print(f"STDOUT: {e.stdout}")
                        print(f"STDERR: {e.stderr}")
                        # Tenta continuar se um falhar
                        continue 
                    except ValueError as e:
                        print(f"Erro de conversão (n={n}, run={i}): Não foi possível converter '{resultado.stdout.strip()}' para float.")
                        continue

                # Calcular média e desvio padrão
                if tempos_ms: # Só calcula se tivermos resultados
                    media = np.mean(tempos_ms)
                    desvio = np.std(tempos_ms)
                    
                    # Escrever no arquivo
                    f_out.write(f"{n},{media},{desvio}\n")
                else:
                    print(f"Nenhum resultado coletado para n={n}")
                    f_out.write(f"{n},ERRO,ERRO\n")

    except IOError as e:
        print(f"Erro ao escrever arquivo de resultados: {e}")
    except Exception as e:
        print(f"Um erro inesperado ocorreu: {e}")

print("Execução dos experimentos concluída.")
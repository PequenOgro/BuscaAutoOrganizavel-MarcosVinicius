import os
import subprocess
import numpy as np
import platform
import sys

# This script is designed to be run from the root of the project directory (e.g., Aed2)

def run_c():
    """Compiles and runs the C language tests."""
    base_dir = "grupo16_BuscaAutoOrganizavel"
    lang = "C"
    exe_suffix = ".exe" if platform.system() == "Windows" else ""
    exe_path = os.path.join(base_dir, 'codigo', 'c', 'busca_c_exec' + exe_suffix)
    
    # --- 1. Compilação ---
    print("--- Iniciando testes para C ---")
    print("Compilando o código C...")
    compile_cmd = f"gcc {os.path.join(base_dir, 'codigo', 'c', 'busca_c.c')} -o {exe_path}"
    try:
        subprocess.run(compile_cmd, shell=True, check=True, capture_output=True, text=True)
        print("Compilação bem-sucedida.")
    except subprocess.CalledProcessError as e:
        print(f"ERRO DE COMPILAÇÃO para C: {e.stderr}")
        # Tenta rodar mesmo assim, pode já existir o .exe
        if not os.path.exists(exe_path):
            return # Aborta se a compilação falhar e não houver executável
        else:
            print("...usando executável pré-existente.")


    # --- 2. Execução e Coleta de Dados ---
    stats_dir = os.path.join(base_dir, "resultados", "estatisticas")
    os.makedirs(stats_dir, exist_ok=True)
    path_resultados = os.path.join(stats_dir, f"resultados_{lang}.csv")
    
    tamanhos = range(10000, 100001, 10000)
    num_execucoes = 50

    try:
        with open(path_resultados, 'w') as f_out:
            f_out.write("n,tempo_ms,desvio\n")
            
            for n in tamanhos:
                print(f"Testando n={n}...")
                tempos_ms = []
                
                for i in range(1, num_execucoes + 1):
                    arquivo_csv = os.path.join(base_dir, f"dados/n{n:06d}", f"run_{i:03d}.csv")
                    cmd_completo = f"{exe_path} \"{arquivo_csv}\""
                    
                    try:
                        resultado = subprocess.run(cmd_completo, shell=True, capture_output=True, text=True, check=True)
                        # A saída do programa C pode usar vírgula como decimal em algumas localidades
                        tempo_str = resultado.stdout.strip().replace(',', '.')
                        tempo = float(tempo_str)
                        tempos_ms.append(tempo)
                    except subprocess.CalledProcessError as e:
                        print(f"  Erro na execução (n={n}, run={i}): {e.stderr}")
                        continue
                    except ValueError:
                        print(f"  Erro de conversão: Não foi possível converter '{resultado.stdout.strip()}' para float.")
                        continue

                if tempos_ms:
                    media = np.mean(tempos_ms)
                    desvio = np.std(tempos_ms)
                    f_out.write(f"{n},{media},{desvio}\n")
                    print(f"  Resultados para n={n}: Média={media:.4f}ms, Desvio={desvio:.4f}ms")
                else:
                    print(f"  Nenhum resultado coletado para n={n}")
                    f_out.write(f"{n},ERRO,ERRO\n")

        print(f"--- Testes para C concluídos. Resultados salvos em {path_resultados} ---")

    except IOError as e:
        print(f"ERRO: Não foi possível escrever no arquivo de resultados: {e}")
    except Exception as e:
        print(f"ERRO INESPERADO: {e}")

if __name__ == "__main__":
    # Adiciona verificação de dependência
    try:
        import numpy
    except ImportError:
        print("A biblioteca 'numpy' é necessária. Tentando instalar...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "numpy"], check=True)
            print("'numpy' instalado com sucesso.")
        except Exception as e:
            print(f"Falha ao instalar 'numpy'. Por favor, instale manualmente: pip install numpy. Erro: {e}")
            sys.exit(1)
    
    run_c()

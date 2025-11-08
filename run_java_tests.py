import os
import subprocess
import numpy as np
import platform
import sys

def run_java():
    """Compiles and runs the Java language tests."""
    base_dir = "grupo16_BuscaAutoOrganizavel"
    lang = "Java"
    
    # --- 1. Compilação ---
    print("--- Iniciando testes para Java ---")
    print("Compilando o código Java...")
    java_code_dir = os.path.join(base_dir, 'codigo', 'java')
    java_file_path = os.path.join(java_code_dir, 'BuscaJava.java')
    compile_cmd = f"javac -d {java_code_dir} {java_file_path}"
    try:
        subprocess.run(compile_cmd, shell=True, check=True, capture_output=True, text=True)
        print("Compilação bem-sucedida.")
    except subprocess.CalledProcessError as e:
        print(f"ERRO DE COMPILAÇÃO para Java: {e.stderr}")
        return

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
                    cmd_completo = f"java -cp {java_code_dir} BuscaJava \"{arquivo_csv}\""
                    
                    try:
                        resultado = subprocess.run(cmd_completo, shell=True, capture_output=True, text=True, check=True)
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

        print(f"--- Testes para Java concluídos. Resultados salvos em {path_resultados} ---")

    except IOError as e:
        print(f"ERRO: Não foi possível escrever no arquivo de resultados: {e}")
    except Exception as e:
        print(f"ERRO INESPERADO: {e}")

if __name__ == "__main__":
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
    
    run_java()

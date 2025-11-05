import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def main():
    """
    Função principal para gerar os gráficos do projeto.
    Este script deve ser executado da pasta raiz (ex: 'Aed2/').
    """
    
    # --- 1. Definir Caminhos ---
    project_folder = "grupo16_BuscaAutoOrganizavel"
    stats_dir = os.path.join(project_folder, "resultados", "estatisticas")
    graphs_dir = os.path.join(project_folder, "resultados", "graficos")

    # Cria a pasta de gráficos se ela não existir
    os.makedirs(graphs_dir, exist_ok=True)
    print(f"Salvando gráficos em: {os.path.abspath(graphs_dir)}")

    # --- 2. Verificar e Carregar os Dados ---
    path_c = os.path.join(stats_dir, "resultados_C.csv")
    path_java = os.path.join(stats_dir, "resultados_Java.csv")
    path_py = os.path.join(stats_dir, "resultados_Python.csv")

    try:
        # Verifique se os arquivos existem ANTES de tentar ler
        for path in [path_c, path_java, path_py]:
            if not os.path.exists(path):
                print(f"Erro: Não foi possível encontrar o arquivo em '{path}'")
                print("Verifique se você está executando este script da pasta raiz 'Aed2/'")
                print("E se os arquivos de resultados existem em '.../estatisticas/'")
                return # Sai da função main se um arquivo faltar
            
            if os.path.getsize(path) == 0:
                print(f"Erro: O arquivo {path} está vazio (0 bytes).")
                print("Execute 'executar_experimentos.py' novamente.")
                return

        df_c = pd.read_csv(path_c)
        df_java = pd.read_csv(path_java)
        df_py = pd.read_csv(path_py)
        
    except pd.errors.EmptyDataError as e:
        print(f"Erro: O arquivo {e.path} está vazio ou mal formatado.")
        print("Verifique o conteúdo do arquivo.")
        return
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao ler os arquivos CSV: {e}")
        return

    print("--- Dados Carregados com Sucesso ---")
    print("\nResultados C:\n", df_c.head())
    print("\nResultados Java:\n", df_java.head())
    print("\nResultados Python:\n", df_py.head())

    # --- 3. Gerar Gráficos ---
    if 'n' not in df_c or 'tempo_ms' not in df_c or 'desvio' not in df_c:
         print("Erro: O CSV de C não contém as colunas esperadas ('n', 'tempo_ms', 'desvio').")
         return
         
    x = df_c['n'] # Eixo X (tamanho do vetor)

    try:
        # Gráfico 1: Desempenho em C
        plt.figure(figsize=(10, 6))
        plt.errorbar(x, df_c['tempo_ms'], yerr=df_c['desvio'], fmt='-o', capsize=5, color='blue')
        plt.title('Desempenho Busca Auto-organizável (Move-to-Front) em C')
        plt.xlabel('Tamanho do Vetor (n)')
        plt.ylabel('Tempo Médio (ms)')
        plt.grid(True)
        plt.savefig(os.path.join(graphs_dir, 'grafico_C.png'))
        plt.close() # Fecha a figura para liberar memória

        # Gráfico 2: Desempenho em Java
        plt.figure(figsize=(10, 6))
        plt.errorbar(x, df_java['tempo_ms'], yerr=df_java['desvio'], fmt='-o', capsize=5, color='orange')
        plt.title('Desempenho Busca Auto-organizável (Move-to-Front) em Java')
        plt.xlabel('Tamanho do Vetor (n)')
        plt.ylabel('Tempo Médio (ms)')
        plt.grid(True)
        plt.savefig(os.path.join(graphs_dir, 'grafico_Java.png'))
        plt.close()

        # Gráfico 3: Desempenho em Python
        plt.figure(figsize=(10, 6))
        plt.errorbar(x, df_py['tempo_ms'], yerr=df_py['desvio'], fmt='-o', capsize=5, color='green')
        plt.title('Desempenho Busca Auto-organizável (Move-to-Front) em Python')
        plt.xlabel('Tamanho do Vetor (n)')
        plt.ylabel('Tempo Médio (ms)')
        plt.grid(True)
        plt.savefig(os.path.join(graphs_dir, 'grafico_Python.png'))
        plt.close()

        # Gráfico 4: Comparativo das três linguagens
        plt.figure(figsize=(10, 6))
        plt.errorbar(x, df_c['tempo_ms'], yerr=df_c['desvio'], fmt='-o', capsize=5, label='C')
        plt.errorbar(x, df_java['tempo_ms'], yerr=df_java['desvio'], fmt='-s', capsize=5, label='Java')
        plt.errorbar(x, df_py['tempo_ms'], yerr=df_py['desvio'], fmt='-^', capsize=5, label='Python')
        
        plt.title('Comparativo de Desempenho (C, Java, Python)')
        plt.xlabel('Tamanho do Vetor (n)')
        plt.ylabel('Tempo Médio (ms)')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(graphs_dir, 'grafico_Comparativo.png'))
        plt.close()

        print("\n--- Todos os 4 gráficos foram salvos com sucesso! ---")

    except Exception as e:
        print(f"Ocorreu um erro ao gerar os gráficos: {e}")


if __name__ == "__main__":
    # Instala as dependências se necessário (opcional, mas útil)
    try:
        import pandas
    except ImportError:
        print("Instalando pandas...")
        os.system(f"{sys.executable} -m pip install pandas")
    
    try:
        import matplotlib
    except ImportError:
        print("Instalando matplotlib...")
        os.system(f"{sys.executable} -m pip install matplotlib")

    main()
"""
Arquivo: codigo/python/busca_py.py
Para executar: python busca_py.py ../../dados/n010000/run_001.csv
"""
import sys
import time
import random

def busca_mtf(vetor: list[int], chave: int) -> int:
    """
    Busca um elemento usando a estratégia Move-to-Front.
    Se encontrado, o elemento é movido para vetor[0].
    Retorna o índice original do elemento, ou -1 se não encontrado.
    """
    try:
        # index() é uma busca linear em C
        idx_original = vetor.index(chave)
        
        # Move-to-Front
        # pop() remove e retorna o item
        item_encontrado = vetor.pop(idx_original)
        # insert() coloca o item no início
        vetor.insert(0, item_encontrado)
        
        return idx_original
    except ValueError:
        # .index() levanta ValueError se o item não for encontrado
        return -1

def main():
    if len(sys.argv) != 2:
        print("Uso: python busca_py.py <caminho_para_csv>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    
    try:
        # --- ETAPA 1: Leitura do Vetor (Fora do Timer) ---
        with open(filepath, 'r') as f:
            line = f.readline().strip()
            # List comprehension para ler o CSV
            vetor = [int(x) for x in line.split(',')]
            n = len(vetor)

        if n == 0:
            print("Arquivo de dados vazio.", file=sys.stderr)
            sys.exit(1)

        # --- ETAPA 2: Geração da Chave (Fora do Timer) ---
        chave_busca: int
        
        if random.randint(0, 1) == 0: # 50% chance de sucesso 
            chave_busca = random.choice(vetor)
        else: # 50% chance de falha 
            # Gera chave em [3n, 4n]
            chave_busca = random.randint(n * 3, n * 4)

        # --- ETAPA 3: Medição de Tempo (Apenas a Busca) ---
        
        # Inicia o timer
        start_time = time.perf_counter()

        # Executa a busca
        busca_mtf(vetor, chave_busca)

        # Para o timer
        end_time = time.perf_counter()
        
        # Calcula o tempo em milissegundos
        time_spent_ms = (end_time - start_time) * 1000

        # Imprime APENAS o tempo [cite: 164-166]
        print(f"{time_spent_ms}")

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em {filepath}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Um erro ocorreu: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
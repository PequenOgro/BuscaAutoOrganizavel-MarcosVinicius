import random
import os

# Tamanhos de vetor 
tamanhos = range(10000, 100001, 10000)
# 50 execuções por tamanho
num_execucoes = 50 

for n in tamanhos:
    dir_path = f"dados/n{n:06d}"
    os.makedirs(dir_path, exist_ok=True)

    for i in range(1, num_execucoes + 1):
        # Seed distinta para cada arquivo [cite: 78]
        random.seed(i) 

        # Gera números aleatórios (ex: entre 0 e n*2)
        vetor = [random.randint(0, n * 2) for _ in range(n)]

        file_path = f"{dir_path}/run_{i:03d}.csv"

        # Salva em linha única, separado por vírgula [cite: 72]
        with open(file_path, 'w') as f:
            f.write(','.join(map(str, vetor)))

print("Geração de dados concluída.")
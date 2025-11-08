/*
Arquivo: codigo/c/busca_c.c
(A flag -lrt é necessária para clock_gettime em algumas versões)
Para executar: ./busca_c_exec ../../dados/n010000/run_001.csv
*/


#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h> // Para time() e clock_gettime
#ifdef _WIN32
#include <windows.h>

#define CLOCK_MONOTONIC 1
int clock_gettime(int clk_id, struct timespec *tp) {
    (void)clk_id; 
    static LARGE_INTEGER freq;
    static int is_freq_initialized = 0;
    if (!is_freq_initialized) {
        QueryPerformanceFrequency(&freq);
        is_freq_initialized = 1;
    }
    LARGE_INTEGER count;
    QueryPerformanceCounter(&count);
    tp->tv_sec = count.QuadPart / freq.QuadPart;
    tp->tv_nsec = (long)(((count.QuadPart % freq.QuadPart) * 1e9) / freq.QuadPart);
    return 0;
}
#endif

 // Função de busca Move-to-Front
// Retorna o índice original se encontrado, -1 se não.
int busca_mtf(int *vetor, int n, int chave) {
    for (int i = 0; i < n; i++) {
        if (vetor[i] == chave) {
            // Item encontrado, agora move para o front
            int item_encontrado = vetor[i]; // Salva o item
            memmove(&vetor[1], &vetor[0], i * sizeof(int)); // Desloca o bloco de memória
            
            // Coloca o item na primeira posição
            vetor[0] = item_encontrado;
            
            return i; // Retorna o índice original
        }
    }
    return -1; // Não encontrado
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Uso: %s <caminho_para_csv>\n", argv[0]);
        return 1;
    }
    
    char *filepath = argv[1];
    FILE *file = fopen(filepath, "r");
    if (file == NULL) {
        perror("Erro ao abrir arquivo");
        return 1;
    }

    // --- ETAPA 1: Leitura do Vetor (Fora do Timer) - Abordagem Padrão C ---
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    if (file_size <= 0) {
        fprintf(stderr, "Arquivo de dados vazio ou erro de leitura de tamanho.\n");
        fclose(file);
        return 1;
    }
    rewind(file);

    char *line_buffer = malloc(file_size + 1);
    if (line_buffer == NULL) {
        perror("Erro de alocação de buffer para o arquivo");
        fclose(file);
        return 1;
    }

    size_t bytes_read = fread(line_buffer, 1, file_size, file);
    line_buffer[bytes_read] = '\0'; // Garante terminação nula
    fclose(file);

    // --- ETAPA 1.5: Parse do Vetor (Fora do Timer) - Abordagem Robusta ---
    int n = 0;
    int capacity = 10; // Capacidade inicial
    int *vetor = malloc(capacity * sizeof(int));
    if (vetor == NULL) {
        perror("Erro de alocação inicial de memória para o vetor");
        free(line_buffer);
        return 1;
    }

    char *token = strtok(line_buffer, ",");
    while (token != NULL) {
        // Ignora tokens vazios (ex: "1,2,,3")
        if (*token == '\0' || *token == '\n' || *token == '\r') {
            token = strtok(NULL, ",");
            continue;
        }
        if (n == capacity) {
            capacity *= 2;
            int *temp = realloc(vetor, capacity * sizeof(int));
            if (temp == NULL) {
                perror("Erro ao realocar memória para o vetor");
                free(vetor);
                free(line_buffer);
                return 1;
            }
            vetor = temp;
        }
        vetor[n++] = atoi(token);
        token = strtok(NULL, ",");
    }
    free(line_buffer); // Libera o buffer da linha

    // --- ETAPA 2: Geração da Chave (Fora do Timer) ---
    srand(time(NULL)); // Seed do gerador aleatório
    int chave_busca;

    // Adiciona verificação para n > 0 para evitar divisão por zero
    if (n > 0 && rand() % 2 == 0) { // 50% chance de sucesso
        int idx_sucesso = rand() % n; // Seguro agora
        chave_busca = vetor[idx_sucesso];
    } else { // 50% chance de falha ou n == 0
        if (n > 0) {
            chave_busca = (rand() % (n + 1)) + (n * 3); // Gera chave em [3n, 4n]
        } else {
            chave_busca = 0; // Define uma chave de busca padrão se o vetor estiver vazio
        }
    }

    // --- ETAPA 3: Medição de Tempo (Apenas a Busca) ---
    struct timespec start, end;
    
    // Inicia o timer
    clock_gettime(CLOCK_MONOTONIC, &start);

    // Executa a busca
    busca_mtf(vetor, n, chave_busca);

    // Para o timer
    clock_gettime(CLOCK_MONOTONIC, &end);

    // Calcula o tempo em milissegundos
double time_spent_ns = (end.tv_sec - start.tv_sec) * 1e9 + (end.tv_nsec - start.tv_nsec);
double time_spent_ms = time_spent_ns / 1e6;

// Imprime no console
printf("%f\n", time_spent_ms);

// Salva em arquivo
FILE *output_file = fopen("../../resultados/resultados_c.csv", "a");
if (output_file != NULL) {
    fprintf(output_file, "%s,%f\n", filepath, time_spent_ms);
    fclose(output_file);
}

// Libera a memória do vetor
free(vetor);
    
    return 0;
}
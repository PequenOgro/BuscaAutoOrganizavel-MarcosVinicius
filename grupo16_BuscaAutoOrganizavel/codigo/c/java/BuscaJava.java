/*
Arquivo: codigo/java/BuscaJava.java
Para compilar: javac BuscaJava.java
Para executar: java BuscaJava ../../dados/n010000/run_001.csv
*/
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Random;

public class BuscaJava {

    /**
     * Busca um elemento usando a estratégia Move-to-Front.
     * Se encontrado, o elemento é movido para vetor[0].
     * @return O índice original do elemento, ou -1 se não encontrado.
     */
    public static int buscaMtf(int[] vetor, int n, int chave) {
        for (int i = 0; i < n; i++) {
            if (vetor[i] == chave) {
                // Item encontrado
                int itemEncontrado = vetor[i];
                
                // Desloca os elementos [0...i-1] para [1...i]
                // System.arraycopy(origem, posOrigem, destino, posDestino, tamanho)
                System.arraycopy(vetor, 0, vetor, 1, i);
                
                // Coloca o item na primeira posição
                vetor[0] = itemEncontrado;
                
                return i; // Retorna o índice original
            }
        }
        return -1; // Não encontrado
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Uso: java BuscaJava ../../dados/n010000/run_001.csv");
            System.exit(1);
        }
        
        String filepath = args[0];
        
        try {
            // --- ETAPA 1: Leitura do Vetor (Fora do Timer) ---
            String line = Files.readString(Paths.get(filepath)).trim();
            String[] tokens = line.split(",");
            int n = tokens.length;
            int[] vetor = new int[n];
            
            for (int i = 0; i < n; i++) {
                vetor[i] = Integer.parseInt(tokens[i]);
            }

            // --- ETAPA 2: Geração da Chave (Fora do Timer) ---
            Random rand = new Random();
            int chaveBusca;

            if (rand.nextBoolean()) { // 50% chance de sucesso 
                int idxSucesso = rand.nextInt(n);
                chaveBusca = vetor[idxSucesso];
            } else { // 50% chance de falha 
                // Gera chave em [3n, 4n]
                chaveBusca = rand.nextInt(n + 1) + (n * 3);
            }

            // --- ETAPA 3: Medição de Tempo (Apenas a Busca) ---
            long startTime = System.nanoTime();

            buscaMtf(vetor, n, chaveBusca);

            long endTime = System.nanoTime();
            
            // Converte nanossegundos para milissegundos
            double timeSpentMs = (endTime - startTime) / 1_000_000.0;

            // Imprime APENAS o tempo [cite: 164-166]
            System.out.println(timeSpentMs);

        } catch (IOException e) {
            System.err.println("Erro ao ler o arquivo: " + e.getMessage());
            System.exit(1);
        } catch (NumberFormatException e) {
            System.err.println("Erro ao formatar número do arquivo: " + e.getMessage());
            System.exit(1);
        }
    }
}
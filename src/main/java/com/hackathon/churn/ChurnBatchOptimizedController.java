package com.hackathon.churn;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/churn")
@Tag(name = "Churn Analytics - Optimized", description = "Endpoints com processamento paralelo otimizado")
public class ChurnBatchOptimizedController {

    @Autowired
    private ChurnRepository repository;

    @Autowired
    private org.springframework.web.client.RestTemplate restTemplate;

    // Configurações de paralelismo
    private static final int THREAD_POOL_SIZE = 20;  // Processa 20 clientes simultaneamente
    private static final int BULK_INSERT_SIZE = 1000; // Insere 1000 por vez no MongoDB
    
    @PostMapping("/batch/optimized")
    @Operation(summary = "Processamento em Lote OTIMIZADO", 
               description = "Processa CSV com threading paralelo (20x mais rápido) + bulk insert MongoDB")
    public ResponseEntity<byte[]> processarLoteOtimizado(@RequestParam("file") MultipartFile file) throws IOException {
        
        if (file.isEmpty()) {
            return ResponseEntity.badRequest().build();
        }

        long startTime = System.currentTimeMillis();
        
        // 1. Ler CSV de entrada
        List<Map<String, String>> clientes = lerCSV(file.getInputStream());
        int totalClientes = clientes.size();
        
        System.out.println("🚀 Iniciando processamento OTIMIZADO de " + totalClientes + " clientes");
        System.out.println("⚙️  Configuração: " + THREAD_POOL_SIZE + " threads paralelas");
        
        // 2. Criar executor para processamento paralelo
        ExecutorService executor = Executors.newFixedThreadPool(THREAD_POOL_SIZE);
        List<CompletableFuture<ChurnData>> futures = new ArrayList<>();
        
        try {
            // 3. Submeter tarefas paralelas
            for (Map<String, String> linha : clientes) {
                CompletableFuture<ChurnData> future = CompletableFuture.supplyAsync(() -> {
                    return processarClienteComIA(linha);
                }, executor);
                futures.add(future);
            }
            
            // 4. Aguardar todas as tarefas completarem
            System.out.println("⏳ Aguardando processamento paralelo...");
            List<ChurnData> resultados = futures.stream()
                    .map(CompletableFuture::join)
                    .collect(Collectors.toList());
            
            // 5. Bulk insert no MongoDB (em lotes de 1000)
            System.out.println("💾 Salvando " + resultados.size() + " resultados no MongoDB (bulk insert)...");
            int saved = 0;
            for (int i = 0; i < resultados.size(); i += BULK_INSERT_SIZE) {
                int end = Math.min(i + BULK_INSERT_SIZE, resultados.size());
                List<ChurnData> batch = resultados.subList(i, end);
                repository.saveAll(batch);
                saved += batch.size();
                System.out.println("  ✅ Salvos: " + saved + "/" + totalClientes);
            }
            
            // 6. Gerar CSV de saída
            System.out.println("📄 Gerando CSV de resultado...");
            StringBuilder csvResultado = new StringBuilder();
            csvResultado.append("clienteId,idade,genero,regiao,valorMensal,tempoAssinaturaMeses,planoAssinatura,metodoPagamento,dispositivoPrincipal,visualizacoesMes,contatosSuporte,avaliacaoPlataforma,avaliacaoConteudoMedia,avaliacaoConteudoUltimoMes,tempoMedioSessaoMin,diasUltimoAcesso,previsao,probabilidade,riscoAlto,modeloUsado\n");
            
            for (ChurnData dados : resultados) {
                csvResultado.append(String.format("%s,%d,%s,%s,%.2f,%d,%s,%s,%s,%d,%d,%.1f,%.1f,%.1f,%d,%d,%s,%.4f,%b,%s\n",
                    dados.getClienteId(),
                    dados.getIdade(),
                    dados.getGenero(),
                    dados.getRegiao(),
                    dados.getValorMensal(),
                    dados.getTempoAssinaturaMeses(),
                    dados.getPlanoAssinatura(),
                    dados.getMetodoPagamento(),
                    dados.getDispositivoPrincipal(),
                    dados.getVisualizacoesMes(),
                    dados.getContatosSuporte(),
                    dados.getAvaliacaoPlataforma(),
                    dados.getAvaliacaoConteudoMedia(),
                    dados.getAvaliacaoConteudoUltimoMes(),
                    dados.getTempoMedioSessaoMin(),
                    dados.getDiasUltimoAcesso(),
                    dados.getPrevisao(),
                    dados.getProbabilidade(),
                    dados.getRiscoAlto(),
                    dados.getModeloUsado()
                ));
            }
            
            long endTime = System.currentTimeMillis();
            long durationSeconds = (endTime - startTime) / 1000;
            double clientesPerSecond = totalClientes / (double) durationSeconds;
            
            System.out.println("✅ PROCESSAMENTO CONCLUÍDO!");
            System.out.println("⏱️  Tempo total: " + durationSeconds + " segundos");
            System.out.println("⚡ Velocidade: " + String.format("%.2f", clientesPerSecond) + " clientes/segundo");
            
            // Retornar CSV
            byte[] csvBytes = csvResultado.toString().getBytes(StandardCharsets.UTF_8);
            
            return ResponseEntity.ok()
                    .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=resultado_optimized_" + totalClientes + ".csv")
                    .contentType(MediaType.parseMediaType("text/csv"))
                    .body(csvBytes);
                    
        } finally {
            executor.shutdown();
        }
    }
    
    private ChurnData processarClienteComIA(Map<String, String> linha) {
        ChurnData dados = mapearParaChurnData(linha);
        
        // Chamar IA com timeout
        String url = "http://localhost:5000/predict";
        try {
            ChurnData resultadoIA = restTemplate.postForObject(url, dados, ChurnData.class);
            if (resultadoIA != null) {
                dados.setPrevisao(resultadoIA.getPrevisao());
                dados.setProbabilidade(resultadoIA.getProbabilidade());
                dados.setRiscoAlto(resultadoIA.getRiscoAlto());
                dados.setModeloUsado(resultadoIA.getModeloUsado());
            }
        } catch (Exception e) {
            // Fallback em caso de erro
            dados.setPrevisao("Erro");
            dados.setProbabilidade(0.0);
            dados.setRiscoAlto(false);
            dados.setModeloUsado("OFFLINE");
        }
        
        return dados;
    }
    
    private List<Map<String, String>> lerCSV(InputStream inputStream) throws IOException {
        List<Map<String, String>> resultado = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8));
        
        String headerLine = reader.readLine();
        if (headerLine == null) return resultado;
        
        String[] headers = headerLine.split(",");
        
        String line;
        while ((line = reader.readLine()) != null) {
            String[] values = line.split(",");
            Map<String, String> row = new HashMap<>();
            for (int i = 0; i < headers.length && i < values.length; i++) {
                row.put(headers[i].trim(), values[i].trim());
            }
            resultado.add(row);
        }
        
        reader.close();
        return resultado;
    }
    
    private ChurnData mapearParaChurnData(Map<String, String> map) {
        ChurnData data = new ChurnData();
        data.setClienteId(map.getOrDefault("clienteId", "UNKNOWN"));
        data.setIdade(Integer.parseInt(map.getOrDefault("idade", "30")));
        data.setGenero(map.getOrDefault("genero", "Masculino"));
        data.setRegiao(map.getOrDefault("regiao", "Sudeste"));
        data.setValorMensal(Double.parseDouble(map.getOrDefault("valorMensal", "29.90")));
        data.setTempoAssinaturaMeses(Integer.parseInt(map.getOrDefault("tempoAssinaturaMeses", "12")));
        data.setPlanoAssinatura(map.getOrDefault("planoAssinatura", "basico"));
        data.setMetodoPagamento(map.getOrDefault("metodoPagamento", "credito"));
        data.setDispositivoPrincipal(map.getOrDefault("dispositivoPrincipal", "mobile"));
        data.setVisualizacoesMes(Integer.parseInt(map.getOrDefault("visualizacoesMes", "20")));
        data.setContatosSuporte(Integer.parseInt(map.getOrDefault("contatosSuporte", "0")));
        data.setAvaliacaoPlataforma(Double.parseDouble(map.getOrDefault("avaliacaoPlataforma", "4.0")));
        data.setAvaliacaoConteudoMedia(Double.parseDouble(map.getOrDefault("avaliacaoConteudoMedia", "4.0")));
        data.setAvaliacaoConteudoUltimoMes(Double.parseDouble(map.getOrDefault("avaliacaoConteudoUltimoMes", "4.0")));
        data.setTempoMedioSessaoMin(Integer.parseInt(map.getOrDefault("tempoMedioSessaoMin", "45")));
        data.setDiasUltimoAcesso(Integer.parseInt(map.getOrDefault("diasUltimoAcesso", "1")));
        return data;
    }
}

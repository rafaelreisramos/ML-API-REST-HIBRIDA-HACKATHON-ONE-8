package com.hackathon.churn;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.util.*;

@RestController
@RequestMapping("/api")
@Tag(name = "System", description = "Endpoints de sistema e monitoramento")
public class SystemController {

    @Autowired
    private ChurnRepository repository;

    @GetMapping("/health")
    @Operation(summary = "Health Check", description = "Verifica o status da API e dependências")
    public ResponseEntity<Map<String, Object>> healthCheck() {
        Map<String, Object> health = new HashMap<>();
        health.put("status", "UP");
        health.put("timestamp", System.currentTimeMillis());
        health.put("service", "ChurnInsight API");
        health.put("version", "2.0.0");

        // Verificar MongoDB
        try {
            long count = repository.count();
            Map<String, Object> mongodb = new HashMap<>();
            mongodb.put("status", "UP");
            mongodb.put("totalDocuments", count);
            health.put("mongodb", mongodb);
        } catch (Exception e) {
            Map<String, String> mongodb = new HashMap<>();
            mongodb.put("status", "DOWN");
            mongodb.put("error", e.getMessage());
            health.put("mongodb", mongodb);
        }

        // Verificar AI Service
        try {
            org.springframework.web.client.RestTemplate restTemplate = new org.springframework.web.client.RestTemplate();
            String aiUrl = "http://localhost:5000/docs";
            restTemplate.getForObject(aiUrl, String.class);
            Map<String, String> ai = new HashMap<>();
            ai.put("status", "UP");
            ai.put("url", "http://localhost:5000");
            health.put("aiService", ai);
        } catch (Exception e) {
            Map<String, String> ai = new HashMap<>();
            ai.put("status", "DOWN");
            ai.put("error", "Cannot reach AI service");
            health.put("aiService", ai);
        }

        return ResponseEntity.ok(health);
    }

    @GetMapping("/stats")
    @Operation(summary = "Estatísticas Agregadas", description = "Retorna métricas consolidadas das análises")
    public ResponseEntity<Map<String, Object>> getStats() {
        List<ChurnData> todas = repository.findAll();

        Map<String, Object> stats = new HashMap<>();
        stats.put("totalAnalisados", todas.size());

        // Contadores
        long totalRiscoAlto = todas.stream().filter(ChurnData::getRiscoAlto).count();
        stats.put("totalRiscoAlto", totalRiscoAlto);
        stats.put("totalRiscoBaixo", todas.size() - totalRiscoAlto);

        // Taxa de churn
        double taxaChurn = todas.isEmpty() ? 0.0 : (totalRiscoAlto * 100.0 / todas.size());
        stats.put("taxaChurnPercentual", Math.round(taxaChurn * 10) / 10.0);

        // Média de probabilidade
        double mediaProbabilidade = todas.stream()
                .filter(d -> d.getProbabilidade() != null)
                .mapToDouble(ChurnData::getProbabilidade)
                .average()
                .orElse(0.0);
        stats.put("probabilidadeMedia", Math.round(mediaProbabilidade * 1000) / 1000.0);

        // Distribuição por plano
        Map<String, Long> porPlano = new HashMap<>();
        todas.forEach(d -> {
            String plano = d.getPlanoAssinatura() != null ? d.getPlanoAssinatura() : "desconhecido";
            porPlano.put(plano, porPlano.getOrDefault(plano, 0L) + 1);
        });
        stats.put("distribuicaoPorPlano", porPlano);

        // Distribuição por região
        Map<String, Long> porRegiao = new HashMap<>();
        todas.forEach(d -> {
            String regiao = d.getRegiao() != null ? d.getRegiao() : "desconhecido";
            porRegiao.put(regiao, porRegiao.getOrDefault(regiao, 0L) + 1);
        });
        stats.put("distribuicaoPorRegiao", porRegiao);

        // Top 5 clientes de maior risco
        List<Map<String, Object>> topRisco = todas.stream()
                .filter(d -> d.getProbabilidade() != null)
                .sorted((a, b) -> Double.compare(b.getProbabilidade(), a.getProbabilidade()))
                .limit(5)
                .map(d -> {
                    Map<String, Object> cliente = new HashMap<>();
                    cliente.put("clienteId", d.getClienteId());
                    cliente.put("probabilidade", d.getProbabilidade());
                    cliente.put("previsao", d.getPrevisao());
                    return cliente;
                })
                .toList();
        stats.put("top5MaiorRisco", topRisco);

        return ResponseEntity.ok(stats);
    }
}

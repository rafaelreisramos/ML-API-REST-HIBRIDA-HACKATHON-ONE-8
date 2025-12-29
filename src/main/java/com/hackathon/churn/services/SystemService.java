package com.hackathon.churn.services;

import com.hackathon.churn.ChurnData;
import com.hackathon.churn.Repository.ChurnRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Service responsável por operações de sistema e monitoramento.
 * Inclui health checks e estatísticas agregadas.
 */
@Service
public class SystemService {

    @Autowired
    private ChurnRepository repository;

    @Value("${ml.service.url:http://localhost:5000}")
    private String mlServiceUrl;

    /**
     * Verifica o status de saúde da API e suas dependências.
     */
    public Map<String, Object> healthCheck() {
        Map<String, Object> health = new HashMap<>();
        health.put("status", "UP");
        health.put("timestamp", System.currentTimeMillis());
        health.put("service", "ChurnInsight API");
        health.put("version", "2.0.0");

        // Verificar MongoDB
        health.put("mongodb", verificarMongoDB());

        // Verificar AI Service
        health.put("aiService", verificarAIService());

        return health;
    }

    /**
     * Verifica o status do MongoDB.
     */
    private Map<String, Object> verificarMongoDB() {
        Map<String, Object> mongodb = new HashMap<>();
        try {
            long count = repository.count();
            mongodb.put("status", "UP");
            mongodb.put("totalDocuments", count);
        } catch (Exception e) {
            mongodb.put("status", "DOWN");
            mongodb.put("error", e.getMessage());
        }
        return mongodb;
    }

    /**
     * Verifica o status do serviço de IA.
     */
    private Map<String, Object> verificarAIService() {
        Map<String, Object> ai = new HashMap<>();
        try {
            RestTemplate restTemplate = new RestTemplate();
            String aiUrl = mlServiceUrl + "/docs";
            restTemplate.getForObject(aiUrl, String.class);
            ai.put("status", "UP");
            ai.put("url", mlServiceUrl);
        } catch (Exception e) {
            ai.put("status", "DOWN");
            ai.put("error", "Cannot reach AI service");
        }
        return ai;
    }

    /**
     * Retorna estatísticas agregadas das análises de churn.
     */
    public Map<String, Object> getStats() {
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
        stats.put("distribuicaoPorPlano", calcularDistribuicaoPorPlano(todas));

        // Distribuição por região
        stats.put("distribuicaoPorRegiao", calcularDistribuicaoPorRegiao(todas));

        // Top 5 clientes de maior risco
        stats.put("top5MaiorRisco", calcularTop5MaiorRisco(todas));

        return stats;
    }

    /**
     * Calcula a distribuição de análises por plano de assinatura.
     */
    private Map<String, Long> calcularDistribuicaoPorPlano(List<ChurnData> dados) {
        Map<String, Long> porPlano = new HashMap<>();
        dados.forEach(d -> {
            String plano = d.getPlanoAssinatura() != null ? d.getPlanoAssinatura() : "desconhecido";
            porPlano.put(plano, porPlano.getOrDefault(plano, 0L) + 1);
        });
        return porPlano;
    }

    /**
     * Calcula a distribuição de análises por região.
     */
    private Map<String, Long> calcularDistribuicaoPorRegiao(List<ChurnData> dados) {
        Map<String, Long> porRegiao = new HashMap<>();
        dados.forEach(d -> {
            String regiao = d.getRegiao() != null ? d.getRegiao() : "desconhecido";
            porRegiao.put(regiao, porRegiao.getOrDefault(regiao, 0L) + 1);
        });
        return porRegiao;
    }

    /**
     * Retorna os 5 clientes com maior probabilidade de churn.
     */
    private List<Map<String, Object>> calcularTop5MaiorRisco(List<ChurnData> dados) {
        return dados.stream()
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
    }
}

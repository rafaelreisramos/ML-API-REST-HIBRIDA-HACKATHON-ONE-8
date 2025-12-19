package com.hackathon.churn;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import java.util.List;

@RestController
@RequestMapping("/api/churn")
@Tag(name = "Churn Analytics", description = "Endpoints REST para gestão de análises de Churn")
public class ChurnRestController {

    @Autowired
    private ChurnRepository repository;

    @Autowired
    private org.springframework.web.client.RestTemplate restTemplate;

    @GetMapping
    @Operation(summary = "Listar todas as análises", description = "Retorna o histórico completo de previsões.")
    public List<ChurnData> listarTodos() {
        return repository.findByAtivoTrue();
    }

    @GetMapping("/{id}")
    @Operation(summary = "Buscar por ID", description = "Retorna os detalhes de uma análise específica.")
    public ChurnData buscarPorId(@PathVariable String id) {
        return repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Análise não encontrada com ID: " + id));
    }

    @PostMapping
    @Operation(summary = "Nova Análise (Previsão)", description = "Recebe dados do cliente, chama a IA para previsão e salva no banco.")
    public ChurnData criarAnalise(@RequestBody @Valid ChurnData input) {

        // Chamada ao Microserviço Python (IA) - Código reutilizado do GraphQL
        String url = "http://localhost:5000/predict";
        try {
            ChurnData resultadoIA = restTemplate.postForObject(url, input, ChurnData.class);

            if (resultadoIA != null) {
                input.setPrevisao(resultadoIA.getPrevisao());
                input.setProbabilidade(resultadoIA.getProbabilidade());
                input.setRiscoAlto(resultadoIA.getRiscoAlto());
                input.setModeloUsado(resultadoIA.getModeloUsado());
            }

        } catch (Exception e) {
            e.printStackTrace();
            input.setModeloUsado("OFFLINE (REST) - Salvo sem previsão");
            input.setPrevisao("Indisponível");
        }

        return repository.save(input);
    }
}

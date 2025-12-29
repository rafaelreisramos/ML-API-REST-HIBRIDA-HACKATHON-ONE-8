package com.hackathon.churn.controller;

import com.hackathon.churn.ChurnData;
import com.hackathon.churn.services.ChurnService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import java.util.List;

/**
 * Controller REST para operações de análise de Churn.
 * Delega toda a lógica de negócio para ChurnService.
 */
@RestController
@RequestMapping("/api/churn")
@Tag(name = "Churn Analytics", description = "Endpoints REST para gestão de análises de Churn")
public class ChurnRestController {

    @Autowired
    private ChurnService churnService;

    @GetMapping
    @Operation(summary = "Listar todas as análises", description = "Retorna o histórico completo de previsões.")
    public List<ChurnData> listarTodos() {
        return churnService.listarAnalises();
    }

    @GetMapping("/{id}")
    @Operation(summary = "Buscar por ID", description = "Retorna os detalhes de uma análise específica.")
    public ChurnData buscarPorId(@PathVariable String id) {
        return churnService.buscarPorId(id)
                .orElseThrow(() -> new RuntimeException("Análise não encontrada com ID: " + id));
    }

    @PostMapping
    @Operation(summary = "Nova Análise (Previsão)", description = "Recebe dados do cliente, chama a IA para previsão e salva no banco.")
    public ChurnData criarAnalise(@RequestBody @Valid ChurnData input) {
        return churnService.registrarAnalise(input);
    }
}

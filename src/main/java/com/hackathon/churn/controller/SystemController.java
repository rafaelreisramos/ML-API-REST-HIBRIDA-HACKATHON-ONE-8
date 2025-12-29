package com.hackathon.churn.controller;

import com.hackathon.churn.services.SystemService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;

import java.util.*;

/**
 * Controller REST para operações de sistema e monitoramento.
 * Delega toda a lógica de negócio para SystemService.
 */
@RestController
@RequestMapping("/api")
@Tag(name = "System", description = "Endpoints de sistema e monitoramento")
public class SystemController {

    @Autowired
    private SystemService systemService;

    @GetMapping("/health")
    @Operation(summary = "Health Check", description = "Verifica o status da API e dependências")
    public ResponseEntity<Map<String, Object>> healthCheck() {
        return ResponseEntity.ok(systemService.healthCheck());
    }

    @GetMapping("/stats")
    @Operation(summary = "Estatísticas Agregadas", description = "Retorna métricas consolidadas das análises")
    public ResponseEntity<Map<String, Object>> getStats() {
        return ResponseEntity.ok(systemService.getStats());
    }
}

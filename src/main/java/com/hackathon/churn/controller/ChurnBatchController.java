package com.hackathon.churn.controller;

import com.hackathon.churn.ChurnData;
import com.hackathon.churn.services.ChurnBatchService;
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

/**
 * Controller REST para processamento em lote de análises de Churn.
 * Delega toda a lógica de negócio para ChurnBatchService.
 */
@RestController
@RequestMapping("/api/churn")
@Tag(name = "Churn Analytics", description = "Endpoints REST para gestão de análises de Churn")
public class ChurnBatchController {

    @Autowired
    private ChurnBatchService churnBatchService;

    @PostMapping("/batch")
    @Operation(summary = "Processamento em Lote", description = "Recebe um CSV com múltiplos clientes, processa cada um via IA e retorna CSV com previsões")
    public ResponseEntity<byte[]> processarLote(@RequestParam("file") MultipartFile file) throws IOException {

        if (file.isEmpty()) {
            return ResponseEntity.badRequest().build();
        }

        // Processar lote usando o service
        List<ChurnData> resultados = churnBatchService.processarLote(file.getInputStream());

        // Gerar CSV de resultado
        String csvResultado = churnBatchService.gerarCSV(resultados);
        byte[] csvBytes = csvResultado.getBytes(StandardCharsets.UTF_8);

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=resultado_churn.csv")
                .contentType(MediaType.parseMediaType("text/csv"))
                .body(csvBytes);
    }

    @DeleteMapping("/reset")
    @Operation(summary = "Arquivar Dashboard (Soft Delete)", description = "Marca todos os registros atuais como inativos e define data de arquivamento. Operação em massa.")
    public ResponseEntity<Map<String, Object>> arquivarDashboard() {
        long startTime = System.currentTimeMillis();

        long arquivados = churnBatchService.arquivarDashboard();

        long duration = System.currentTimeMillis() - startTime;

        Map<String, Object> response = new HashMap<>();
        response.put("message", "Dashboard arquivado com sucesso.");
        response.put("adicionadosAoArquivo", arquivados);
        response.put("tempoExecucaoMs", duration);

        return ResponseEntity.ok(response);
    }
}

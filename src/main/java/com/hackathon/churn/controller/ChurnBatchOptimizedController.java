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
 * Controller REST para processamento em lote OTIMIZADO de análises de Churn.
 * Utiliza processamento paralelo para maior performance.
 * Delega toda a lógica de negócio para ChurnBatchService.
 */
@RestController
@RequestMapping("/api/churn")
@Tag(name = "Churn Analytics - Optimized", description = "Endpoints com processamento paralelo otimizado")
public class ChurnBatchOptimizedController {

    @Autowired
    private ChurnBatchService churnBatchService;

    @PostMapping("/batch/optimized")
    @Operation(summary = "Processamento em Lote OTIMIZADO", description = "Processa CSV com threading paralelo (20x mais rápido) + bulk insert MongoDB")
    public ResponseEntity<byte[]> processarLoteOtimizado(@RequestParam("file") MultipartFile file) throws IOException {

        if (file.isEmpty()) {
            return ResponseEntity.badRequest().build();
        }

        long startTime = System.currentTimeMillis();

        // Processar lote otimizado usando o service
        List<ChurnData> resultados = churnBatchService.processarLoteOtimizado(file.getInputStream());

        // Gerar CSV de resultado
        String csvResultado = churnBatchService.gerarCSV(resultados);

        long endTime = System.currentTimeMillis();
        long durationSeconds = (endTime - startTime) / 1000;
        double clientesPerSecond = resultados.size() / (double) Math.max(durationSeconds, 1);

        System.out.println("✅ PROCESSAMENTO CONCLUÍDO!");
        System.out.println("⏱️  Tempo total: " + durationSeconds + " segundos");
        System.out.println("⚡ Velocidade: " + String.format("%.2f", clientesPerSecond) + " clientes/segundo");

        byte[] csvBytes = csvResultado.getBytes(StandardCharsets.UTF_8);

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION,
                        "attachment; filename=resultado_optimized_" + resultados.size() + ".csv")
                .contentType(MediaType.parseMediaType("text/csv"))
                .body(csvBytes);
    }
}

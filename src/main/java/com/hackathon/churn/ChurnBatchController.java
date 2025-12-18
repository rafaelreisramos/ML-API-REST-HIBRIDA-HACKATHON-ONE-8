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

@RestController
@RequestMapping("/api/churn")
@Tag(name = "Churn Analytics", description = "Endpoints REST para gestão de análises de Churn")
public class ChurnBatchController {

    @Autowired
    private ChurnRepository repository;

    @Autowired
    private org.springframework.web.client.RestTemplate restTemplate;

    @PostMapping("/batch")
    @Operation(summary = "Processamento em Lote", description = "Recebe um CSV com múltiplos clientes, processa cada um via IA e retorna CSV com previsões")
    public ResponseEntity<byte[]> processarLote(@RequestParam("file") MultipartFile file) throws IOException {

        if (file.isEmpty()) {
            return ResponseEntity.badRequest().build();
        }

        // Ler CSV de entrada
        List<Map<String, String>> clientes = lerCSV(file.getInputStream());

        // Processar cada linha
        StringBuilder csvResultado = new StringBuilder();
        csvResultado.append(
                "clienteId,idade,genero,regiao,valorMensal,tempoAssinaturaMeses,planoAssinatura,metodoPagamento,dispositivoPrincipal,visualizacoesMes,contatosSuporte,avaliacaoPlataforma,avaliacaoConteudoMedia,avaliacaoConteudoUltimoMes,tempoMedioSessaoMin,diasUltimoAcesso,previsao,probabilidade,riscoAlto,modeloUsado\n");

        for (Map<String, String> linha : clientes) {
            try {
                ChurnData dados = mapearParaChurnData(linha);

                // Chamar IA
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
                    dados.setPrevisao("Erro");
                    dados.setProbabilidade(0.0);
                    dados.setRiscoAlto(false);
                    dados.setModeloUsado("OFFLINE");
                }

                // Salvar no MongoDB
                repository.save(dados);

                // Adicionar ao CSV de saída
                csvResultado
                        .append(String.format("%s,%d,%s,%s,%.2f,%d,%s,%s,%s,%d,%d,%.1f,%.1f,%.1f,%d,%d,%s,%.4f,%b,%s\n",
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
                                dados.getModeloUsado()));

            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        // Retornar CSV com resultados
        byte[] csvBytes = csvResultado.toString().getBytes(StandardCharsets.UTF_8);

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=resultado_churn.csv")
                .contentType(MediaType.parseMediaType("text/csv"))
                .body(csvBytes);
    }

    private List<Map<String, String>> lerCSV(InputStream inputStream) throws IOException {
        List<Map<String, String>> resultado = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8));

        String headerLine = reader.readLine();
        if (headerLine == null)
            return resultado;

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

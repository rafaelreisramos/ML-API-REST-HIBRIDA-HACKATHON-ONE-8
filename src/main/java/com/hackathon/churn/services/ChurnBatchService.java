package com.hackathon.churn.services;

import com.hackathon.churn.ChurnData;
import com.hackathon.churn.Repository.ChurnRepository;
import org.springframework.beans.factory.annotation.Autowired;
import com.hackathon.churn.Repository.ChurnRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.Collectors;

/**
 * Service responsável pelo processamento em lote de análises de Churn.
 * Inclui leitura de CSV, processamento paralelo e operações em massa.
 */
@Service
public class ChurnBatchService {

    @Autowired
    private ChurnRepository repository;

    @Autowired
    private ChurnService churnService;

    // Configurações de paralelismo
    private static final int THREAD_POOL_SIZE = 20;
    private static final int BULK_INSERT_SIZE = 1000;

    /**
     * Processa um lote de clientes a partir de um CSV (processamento sequencial).
     */
    public List<ChurnData> processarLote(InputStream csvInputStream) throws IOException {
        List<Map<String, String>> clientes = lerCSV(csvInputStream);
        List<ChurnData> resultados = new ArrayList<>();

        for (Map<String, String> linha : clientes) {
            try {
                ChurnData dados = mapearParaChurnData(linha);
                ChurnData resultado = churnService.chamarServicoIA(dados);
                repository.save(resultado);
                resultados.add(resultado);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        return resultados;
    }

    /**
     * Processa um lote de clientes com processamento paralelo otimizado.
     */
    public List<ChurnData> processarLoteOtimizado(InputStream csvInputStream) throws IOException {
        List<Map<String, String>> clientes = lerCSV(csvInputStream);
        int totalClientes = clientes.size();

        System.out.println("🚀 Iniciando processamento OTIMIZADO de " + totalClientes + " clientes");
        System.out.println("⚙️  Configuração: " + THREAD_POOL_SIZE + " threads paralelas");

        ExecutorService executor = Executors.newFixedThreadPool(THREAD_POOL_SIZE);
        List<CompletableFuture<ChurnData>> futures = new ArrayList<>();

        try {
            // Submeter tarefas paralelas
            for (Map<String, String> linha : clientes) {
                CompletableFuture<ChurnData> future = CompletableFuture.supplyAsync(() -> {
                    ChurnData dados = mapearParaChurnData(linha);
                    return churnService.chamarServicoIA(dados);
                }, executor);
                futures.add(future);
            }

            // Aguardar todas as tarefas completarem
            System.out.println("⏳ Aguardando processamento paralelo...");
            List<ChurnData> resultados = futures.stream()
                    .map(CompletableFuture::join)
                    .collect(Collectors.toList());

            // Bulk insert no MongoDB
            salvarEmLote(resultados, totalClientes);

            return resultados;

        } finally {
            executor.shutdown();
        }
    }

    /**
     * Salva resultados em lotes para melhor performance.
     */
    private void salvarEmLote(List<ChurnData> resultados, int totalClientes) {
        System.out.println("💾 Salvando " + resultados.size() + " resultados no Banco de Dados (bulk insert)...");
        int saved = 0;

        for (int i = 0; i < resultados.size(); i += BULK_INSERT_SIZE) {
            int end = Math.min(i + BULK_INSERT_SIZE, resultados.size());
            List<ChurnData> batch = resultados.subList(i, end);
            repository.saveAll(batch);
            saved += batch.size();
            System.out.println("  ✅ Salvos: " + saved + "/" + totalClientes);
        }
    }

    /**
     * Arquiva todas as análises ativas (soft delete).
     * Retorna o número de registros arquivados.
     */
    public long arquivarDashboard() {
        // Implementação JPA para Soft Delete em Lote
        List<ChurnData> ativos = repository.findByAtivoTrue();
        long count = ativos.size();

        if (count > 0) {
            LocalDateTime agora = LocalDateTime.now();
            ativos.forEach(d -> {
                d.setAtivo(false);
                d.setDataArquivamento(agora);
            });
            repository.saveAll(ativos);
        }

        return count;
    }

    /**
     * Gera o conteúdo CSV a partir de uma lista de análises.
     */
    public String gerarCSV(List<ChurnData> resultados) {
        StringBuilder csv = new StringBuilder();
        csv.append(
                "clienteId,idade,genero,regiao,valorMensal,tempoAssinaturaMeses,planoAssinatura,metodoPagamento,dispositivoPrincipal,visualizacoesMes,contatosSuporte,avaliacaoPlataforma,avaliacaoConteudoMedia,avaliacaoConteudoUltimoMes,tempoMedioSessaoMin,diasUltimoAcesso,tipoContrato,categoriaFavorita,acessibilidade,previsao,probabilidade,riscoAlto,modeloUsado\n");

        for (ChurnData dados : resultados) {
            csv.append(String.format(Locale.US,
                    "%s,%d,%s,%s,%.2f,%d,%s,%s,%s,%d,%d,%.1f,%.1f,%.1f,%d,%d,%s,%s,%d,%s,%.4f,%b,%s\n",
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
                    // Novos
                    dados.getTipoContrato(),
                    dados.getCategoriaFavorita(),
                    dados.getAcessibilidade(),
                    // Outputs
                    dados.getPrevisao(),
                    dados.getProbabilidade(),
                    dados.getRiscoAlto(),
                    dados.getModeloUsado()));
        }

        return csv.toString();
    }

    /**
     * Lê um arquivo CSV e retorna uma lista de mapas com os dados.
     */
    public List<Map<String, String>> lerCSV(InputStream inputStream) throws IOException {
        List<Map<String, String>> resultado = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8));

        String headerLine = reader.readLine();
        if (headerLine == null) {
            reader.close();
            return resultado;
        }

        String[] headers = headerLine.split(",");

        // Remove BOM se existir (comum em arquivos Windows/Excel)
        if (headers.length > 0 && headers[0].startsWith("\uFEFF")) {
            headers[0] = headers[0].substring(1);
        }

        // Trim headers
        for (int i = 0; i < headers.length; i++)
            headers[i] = headers[i].trim();

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

    /**
     * Mapeia um mapa de strings para um objeto ChurnData.
     */
    public ChurnData mapearParaChurnData(Map<String, String> map) {
        ChurnData data = new ChurnData();
        data.setAtivo(true);
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

        // Novos Campos V8
        data.setTipoContrato(map.getOrDefault("tipoContrato", "MENSAL"));
        data.setCategoriaFavorita(map.getOrDefault("categoriaFavorita", "FILMES"));
        data.setAcessibilidade(Integer.parseInt(map.getOrDefault("acessibilidade", "0")));

        return data;
    }
}

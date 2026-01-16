package com.hackathon.churn.services;

import com.hackathon.churn.ChurnData;
import com.hackathon.churn.Repository.ChurnRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Optional;
import org.springframework.beans.BeanUtils;
import java.util.stream.Collectors;

/**
 * Service responsável pela lógica de negócio de análises de Churn.
 * Centraliza operações de CRUD e integração com o serviço de IA.
 */
@Service

public class ChurnService {

    @Autowired
    private ChurnRepository repository;

    @Autowired
    private com.hackathon.churn.Repository.secondary.ChurnRepositorySecondary repositorySecondary;

    @Autowired
    private RestTemplate restTemplate;

    @Value("${ml.service.url:http://localhost:5000}")
    private String mlServiceUrl;

    private ChurnData clonar(ChurnData origem) {
        ChurnData copia = new ChurnData();
        BeanUtils.copyProperties(origem, copia);
        return copia;
    }

    /**
     * Lista todas as análises ativas.
     */
    public List<ChurnData> listarAnalises() {
        return repository.findByAtivoTrue();
    }

    /**
     * Lista análises com risco alto de churn.
     */
    public List<ChurnData> listarRiscoAlto() {
        return repository.findByRiscoAltoTrue();
    }

    /**
     * Busca uma análise pelo ID.
     */
    public Optional<ChurnData> buscarPorId(String id) {
        return repository.findById(id);
    }

    /**
     * Registra uma nova análise de churn.
     * Chama o serviço de IA para obter a previsão e salva no banco.
     */
    public ChurnData registrarAnalise(ChurnData input) {
        // Garantir que novos registros sejam ativos
        input.setAtivo(true);

        // Chamar serviço de IA para previsão
        ChurnData resultado = chamarServicoIA(input);

        // Salvar no banco
        ChurnData salvo = repository.save(resultado);

        // Espelhamento para banco secundário (Fail-safe)
        try {
            repositorySecondary.save(clonar(salvo));
        } catch (Exception e) {
            System.err.println("Erro ao salvar no banco secundário: " + e.getMessage());
        }

        return salvo;
    }

    /**
     * Chama o microserviço Python de IA para obter previsão de churn.
     * Em caso de falha, retorna os dados com status offline.
     */
    public ChurnData chamarServicoIA(ChurnData dados) {
        String url = mlServiceUrl + "/predict";

        try {
            ChurnData resultadoIA = restTemplate.postForObject(url, dados, ChurnData.class);

            if (resultadoIA != null) {
                dados.setPrevisao(resultadoIA.getPrevisao());
                dados.setProbabilidade(resultadoIA.getProbabilidade());
                dados.setRiscoAlto(resultadoIA.getRiscoAlto());
                dados.setModeloUsado(resultadoIA.getModeloUsado());
            }

        } catch (Exception e) {
            e.printStackTrace();
            dados.setModeloUsado("OFFLINE - Salvo sem previsão");
            dados.setPrevisao("Indisponível");
            dados.setProbabilidade(0.0);
            dados.setRiscoAlto(false);
        }

        return dados;
    }

    /**
     * Salva uma análise no banco de dados.
     */
    public ChurnData salvar(ChurnData dados) {
        ChurnData salvo = repository.save(dados);
        try {
            repositorySecondary.save(clonar(salvo));
        } catch (Exception e) {
            System.err.println("Erro ao salvar no banco secundário (salvar): " + e.getMessage());
        }
        return salvo;
    }

    /**
     * Salva múltiplas análises em lote.
     */
    public List<ChurnData> salvarTodos(List<ChurnData> dados) {
        List<ChurnData> salvos = repository.saveAll(dados);
        try {
            List<ChurnData> copias = salvos.stream()
                    .map(this::clonar)
                    .collect(Collectors.toList());
            repositorySecondary.saveAll(copias);
        } catch (Exception e) {
            System.err.println("Erro ao salvar lote no banco secundário: " + e.getMessage());
        }
        return salvos;
    }
}

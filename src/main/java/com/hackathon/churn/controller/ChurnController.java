package com.hackathon.churn.controller;

import com.hackathon.churn.ChurnData;
import com.hackathon.churn.Repository.ChurnRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;
import jakarta.validation.Valid;
import java.util.List;

@Controller
public class ChurnController {

    @Autowired
    private ChurnRepository repository;

    @QueryMapping
    public List<ChurnData> listarAnalises() {
        return repository.findByAtivoTrue();
    }

    @QueryMapping
    public List<ChurnData> listarRiscoAlto() {
        return repository.findByRiscoAltoTrue();
    }

    @QueryMapping
    public ChurnData buscarPorId(@Argument String id) {
        return repository.findById(id).orElse(null);
    }

    @Autowired
    private org.springframework.web.client.RestTemplate restTemplate;

    @MutationMapping
    public ChurnData registrarAnalise(@Argument @Valid ChurnData input) {

        // Chamada ao Microserviço Python (IA)
        String url = "http://localhost:5000/predict";
        try {
            // O RestTemplate serializa o 'input' para JSON e envia para o Python.
            // O Python retorna um JSON que é deserializado de volta para ChurnData (ou um
            // DTO parcial).
            // Aqui estamos assumindo que o retorno tem os campos de resultado preenchidos.

            ChurnData resultadoIA = restTemplate.postForObject(url, input, ChurnData.class);

            if (resultadoIA != null) {
                input.setPrevisao(resultadoIA.getPrevisao());
                input.setProbabilidade(resultadoIA.getProbabilidade());
                input.setRiscoAlto(resultadoIA.getRiscoAlto());
                input.setModeloUsado(resultadoIA.getModeloUsado());
            }

        } catch (Exception e) {
            e.printStackTrace();
            input.setModeloUsado("OFFLINE - Salvo sem previsão");
            input.setPrevisao("Indisponível");
        }

        return repository.save(input);
    }
}

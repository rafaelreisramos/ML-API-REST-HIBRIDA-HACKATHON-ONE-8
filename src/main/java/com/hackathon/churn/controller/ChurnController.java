package com.hackathon.churn.controller;

import com.hackathon.churn.ChurnData;
import com.hackathon.churn.services.ChurnService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.MutationMapping;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;
import jakarta.validation.Valid;
import java.util.List;

/**
 * Controller GraphQL para operações de análise de Churn.
 * Delega toda a lógica de negócio para ChurnService.
 */
@Controller
public class ChurnController {

    @Autowired
    private ChurnService churnService;

    @QueryMapping
    public List<ChurnData> listarAnalises() {
        return churnService.listarAnalises();
    }

    @QueryMapping
    public List<ChurnData> listarRiscoAlto() {
        return churnService.listarRiscoAlto();
    }

    @QueryMapping
    public ChurnData buscarPorId(@Argument String id) {
        return churnService.buscarPorId(id).orElse(null);
    }

    @MutationMapping
    public ChurnData registrarAnalise(@Argument @Valid ChurnData input) {
        return churnService.registrarAnalise(input);
    }
}

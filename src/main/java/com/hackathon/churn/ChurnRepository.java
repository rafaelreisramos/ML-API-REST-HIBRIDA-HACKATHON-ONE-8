package com.hackathon.churn;

import org.springframework.data.mongodb.repository.MongoRepository;
import java.util.List;

public interface ChurnRepository extends MongoRepository<ChurnData, String> {

    // Método mágico: O Spring implementa sozinho baseado no nome!
    List<ChurnData> findByRiscoAltoTrue();

    // Buscar por ID do cliente original
    List<ChurnData> findByClienteId(String clienteId);
}

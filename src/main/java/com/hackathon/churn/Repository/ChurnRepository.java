package com.hackathon.churn.Repository;

import com.hackathon.churn.ChurnData;
import org.springframework.data.mongodb.repository.MongoRepository;
import java.util.List;

public interface ChurnRepository extends MongoRepository<ChurnData, String> {


    List<ChurnData> findByRiscoAltoTrue();

    List<ChurnData> findByClienteId(String clienteId);

    List<ChurnData> findByAtivoTrue();
}

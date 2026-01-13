package com.hackathon.churn.Repository;

import com.hackathon.churn.ChurnData;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface ChurnRepository extends JpaRepository<ChurnData, String> {

    List<ChurnData> findByRiscoAltoTrue();

    List<ChurnData> findByClienteId(String clienteId);

    List<ChurnData> findByAtivoTrue();
}

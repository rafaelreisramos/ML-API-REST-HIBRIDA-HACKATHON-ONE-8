package com.hackathon.churn.Repository.secondary;

import com.hackathon.churn.ChurnData;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ChurnRepositorySecondary extends JpaRepository<ChurnData, String> {
}

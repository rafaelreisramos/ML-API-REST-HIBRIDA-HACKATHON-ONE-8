package com.hackathon.churn.Repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.hackathon.churn.usuario.Usuario;

import java.util.Optional;

public interface UsuarioRepository extends JpaRepository<Usuario, String> {

    Usuario findByLogin(String login);

}

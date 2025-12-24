package com.hackathon.churn.configurations;

import com.hackathon.churn.Repository.UsuarioRepository;
import com.hackathon.churn.usuario.Usuario;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.crypto.password.PasswordEncoder;


@Configuration
public class DataInitializer {

    @Bean
    CommandLineRunner initUsuarios(
            UsuarioRepository usuarioRepository,
            PasswordEncoder passwordEncoder) {


        return args -> {
            if (usuarioRepository.findByLogin("admin") == null) {

                Usuario usuario = new Usuario();
                usuario.setLogin("admin");
                usuario.setSenha(passwordEncoder.encode("123456"));

                usuarioRepository.save(usuario);

            }
        };
    }
}


package com.hackathon.churn.services;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.exceptions.JWTCreationException;
import com.auth0.jwt.exceptions.JWTVerificationException;
import org.springframework.stereotype.Service;
import com.hackathon.churn.usuario.Usuario;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;

@Service
public class TokenService {


    public static final String usuarioToken = System.getenv("JWT_TOKEN");

    public String gerarToken(Usuario usuario){
        try{
            var algoritimo = Algorithm.HMAC256(usuarioToken);
            return JWT.create()
                    .withIssuer("API-REST-HIBRIDA-HACKATHON-ONE-8")
                    .withSubject(usuario.getLogin())
                    .withExpiresAt(dataExpiracao())
                    .sign(algoritimo);
        }catch (JWTCreationException e){
            throw new RuntimeException("Erro ao gerar token" , e);
        }
    }

    public String getSubject(String tokenJWT){
        try{
            var algoritimo = Algorithm.HMAC256(usuarioToken);
            return JWT.require(algoritimo)
                    .withIssuer("API-REST-HIBRIDA-HACKATHON-ONE-8")
                    .build()
                    .verify(tokenJWT)
                    .getSubject();
        }catch (JWTVerificationException e){
            throw new RuntimeException("Token inválido ou expirado");
        }
    }

    private Instant dataExpiracao(){
        return (LocalDateTime.now().plusHours(1).toInstant(ZoneOffset.of("-03:00")));
    }

}

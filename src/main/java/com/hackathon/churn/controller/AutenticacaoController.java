package com.hackathon.churn.controller;

import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.hackathon.churn.security.DadosTokenJWT;
import com.hackathon.churn.services.TokenService;
import com.hackathon.churn.usuario.DadosUsuario;
import com.hackathon.churn.usuario.Usuario;

@RestController
@RequestMapping("/login")
public class AutenticacaoController {

    @Autowired
    private AuthenticationManager manager;

    @Autowired
    private TokenService tokenService;

    @PostMapping
    public ResponseEntity logarUsuario(@RequestBody @Valid DadosUsuario dadosUsuario){
        var authenticationToken = new UsernamePasswordAuthenticationToken(dadosUsuario.login(), dadosUsuario.senha());
        var authentication = manager.authenticate(authenticationToken);

        var token = tokenService.gerarToken((Usuario) authentication.getPrincipal());

        return ResponseEntity.ok(new DadosTokenJWT(token));
    }

}

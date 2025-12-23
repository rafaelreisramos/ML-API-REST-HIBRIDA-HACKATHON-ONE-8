package com.hackathon.churn.Repository;

import org.bson.types.ObjectId;
import org.springframework.data.mongodb.repository.MongoRepository;
import com.hackathon.churn.usuario.Usuario;

import java.util.Optional;

public interface UsuarioRepository extends MongoRepository<Usuario, ObjectId> {

    Usuario findByLogin(String login);

}

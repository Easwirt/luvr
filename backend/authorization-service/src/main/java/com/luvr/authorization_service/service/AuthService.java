package com.luvr.authorization_service.service;


import com.luvr.authorization_service.entity.UserRequest;
import com.luvr.authorization_service.exception.UserException;
import com.luvr.authorization_service.repository.AuthRepository;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

import java.util.HashMap;
import java.util.Map;

@Service
public class AuthService {

    private final AuthRepository authRepository;
    private final JwtService jwtService;

    public AuthService(AuthRepository authRepository, JwtService jwtService) {
        this.authRepository = authRepository;
        this.jwtService = jwtService;
    }

    public Mono<String> createUser(String email, String username, String password) throws UserException {
        return authRepository.createUser(email, username, password);
    }

    public Mono<?> login(String email) throws UserException {
        UserRequest userRequest = authRepository.login(email).block();

        Map<String,String> tokens=new HashMap<>();

        if (userRequest != null) {
            String accessToken=jwtService.generateAccessToken(userRequest.username(), "user");
            String refreshToken=jwtService.generateRefreshToken(userRequest.username(), "user");
            tokens.put("accessToken",accessToken);
            tokens.put("refreshToken",refreshToken);
            return Mono.just(tokens);
        }
        else {
            return Mono.error(new UserException("User not found"));
        }

    }







}

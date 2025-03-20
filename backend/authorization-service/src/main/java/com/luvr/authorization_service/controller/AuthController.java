package com.luvr.authorization_service.controller;

import com.luvr.authorization_service.entity.AuthRequest;
import com.luvr.authorization_service.entity.RefreshTokenRequest;
import com.luvr.authorization_service.exception.JwtException;
import com.luvr.authorization_service.exception.UserException;
import com.luvr.authorization_service.service.AuthService;
import com.luvr.authorization_service.service.JwtService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private final AuthService authService;
    private final JwtService jwtService;


    @Autowired
    public AuthController(AuthService authService, JwtService jwtService) {
        this.authService = authService;
        this.jwtService = jwtService;
    }


    @PostMapping("/register")
    public Mono<ResponseEntity<String>> registerUser(@RequestBody AuthRequest user) {
        return authService.createUser(user.getEmail(), user.getUsername(), user.getPassword())
                .map(ResponseEntity::ok)
                .onErrorResume(UserException.class, e ->
                        Mono.just(ResponseEntity.badRequest().body("Registration failed: " + e.getMessage()))
                );
    }



    @PostMapping("/login")
    public ResponseEntity<String> loginUser(@RequestBody AuthRequest user) {
        try {
            String token = authService.login(user.getEmail()).block().toString();
            return ResponseEntity.ok(token);
        } catch (JwtException e) {
            return ResponseEntity.status(401).body("Login failed: " + e.getMessage());
        }
    }

    @PostMapping("/refresh")
    public ResponseEntity<String> refreshToken(@RequestBody RefreshTokenRequest refreshTokenDto) {
        String refreshToken = refreshTokenDto.getRefreshToken();
        if (jwtService.validateToken(refreshToken)) {
            String username=jwtService.extractUsername(refreshToken);
            String newAccessToken=jwtService.generateAccessToken(username,"user");
            return ResponseEntity.ok(newAccessToken);
        }
        return ResponseEntity.badRequest().body("Refresh token expired, please login again");
    }




}

package com.luvr.authorization_service.service;

import com.luvr.authorization_service.exception.JwtException;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import javax.crypto.SecretKey;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

@Service
public class JwtService {

    @Value("${jwt.secret}")
    private String secret;

    private SecretKey key;

    @PostConstruct
    public void initKey() {
        this.key = Keys.hmacShaKeyFor(secret.getBytes());
    }


    public String generateToken(String name, String role, String tokenType, long expiration) throws JwtException {
        Map<String, Object> claims=new HashMap<>();
        claims.put("name", name);
        claims.put("role", role);
        claims.put("tokenType", tokenType);

        return Jwts.builder()
                .claims()
                .add(claims)
                .subject(name)
                .issuedAt(new Date(System.currentTimeMillis()))
                .expiration(new Date(System.currentTimeMillis() + 1000 * 60 * expiration))
                .and()
                .signWith(getKey())
                .compact();
    }

    public String generateAccessToken(String name, String role) {
        return generateToken(name, role, "access", 5);
    }

    public String generateRefreshToken(String name, String role) {
        return generateToken(name, role, "refresh", 60);
    }

    private SecretKey getKey() {
        return key;
    }

    public boolean validateToken(String token) {
        try {
            Jwts.parser().setSigningKey(getKey()).build().parseClaimsJws(token);
            return true;
        } catch (JwtException e) {
            return false;
        }
    }

    public String extractUsername(String token) {
        return extractClaim(token, Claims::getSubject);
    }


    private Claims extractAllClaims(String token) {
        return Jwts.parser()
                .verifyWith(getKey())
                .build()
                .parseSignedClaims(token)
                .getPayload();
    }

    private <T> T extractClaim(String token, Function<Claims, T> claimsResolver) {
        Claims claims = Jwts.parser().setSigningKey(getKey()).build()
                .parseClaimsJws(token).getBody();
        return claimsResolver.apply(claims);
    }



}
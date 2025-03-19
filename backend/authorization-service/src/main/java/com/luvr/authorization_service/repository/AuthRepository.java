package com.luvr.authorization_service.repository;

import com.luvr.authorization_service.entity.UserRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.cloud.client.discovery.DiscoveryClient;
import org.springframework.stereotype.Repository;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Repository
public class AuthRepository {

    private final WebClient.Builder webClientBuilder;

    private final DiscoveryClient discoveryClient;

    @Autowired
    public AuthRepository(WebClient.Builder webClientBuilder, DiscoveryClient discoveryClient) {
        this.webClientBuilder = webClientBuilder;
        this.discoveryClient = discoveryClient;
    }

    public Mono<String> createUser(String email, String username, String password) {
        String serviceUrl = discoveryClient.getInstances("user-service")
                .stream()
                .findFirst()
                .map(serviceInstance -> serviceInstance.getUri().toString())
                .orElseThrow(() -> new RuntimeException("No service available"));

        return webClientBuilder.baseUrl(serviceUrl)
                .build()
                .post()
                .uri("/users")
                .bodyValue(new UserRequest(email, username, password))
                .retrieve()
                .bodyToMono(String.class);
    }

    public Mono<UserRequest> login(String email) {
        String serviceUrl = discoveryClient.getInstances("user-service")
                .stream()
                .findFirst()
                .map(serviceInstance -> serviceInstance.getUri().toString())
                .orElseThrow(() -> new RuntimeException("No service available"));

        return webClientBuilder.baseUrl(serviceUrl)
                .build()
                .get()
                .uri("/users/{email}", email)
                .retrieve()
                .bodyToMono(UserRequest.class);
    }

}

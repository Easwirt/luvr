package com.luvr.authorization_service.entity;

public record UserRequest(String email, String username, String password) {
}
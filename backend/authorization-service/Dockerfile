FROM maven:3.8.4-openjdk-17-slim AS build
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -B

COPY src ./src
RUN mvn -B -DskipTests clean package

FROM openjdk:17-jdk-alpine
WORKDIR /app

COPY --from=build /app/target/authorization-service-0.0.1-SNAPSHOT.jar /app/authorization-service.jar


EXPOSE 8081

ENTRYPOINT ["java", "-jar", "authorization-service.jar"]
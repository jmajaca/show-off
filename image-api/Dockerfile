FROM arm64v8/openjdk:17.0.2-jdk-oracle
ARG JAR_FILE=build/libs/*.jar
COPY ${JAR_FILE} app.jar
ENTRYPOINT java -jar /app.jar

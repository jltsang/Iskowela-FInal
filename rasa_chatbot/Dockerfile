# Start from the base image
FROM rasa/rasa:3.5.10

# Set the working directory
WORKDIR /app
COPY . /app
USER root

# Copy the Rasa project directory
COPY ./data /app/data
COPY config.yml /app
COPY endpoints.yml /app

# Train the Rasa model
RUN rasa train

VOLUME /app
VOLUME /app/data
VOLUME /app/models

# Set the entrypoint command
CMD ["run", "-m", "/app/models", "--enable-api","--cors","*","--debug" ,"--endpoints", "endpoints.yml", "--log-file", "out.log", "--debug"]

# Expose the necessary ports
EXPOSE 5005
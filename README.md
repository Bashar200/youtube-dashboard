# FastAPI Microservice to fetch YouTube Data

This is a FastAPI-based microservice that integrates with MongoDB and Kafka. It provides an background thread to hit an API at an interval of 1 minute and includes a GET API with search functionality and another API to regsiter google api keys if exhausted.

## Features

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **MongoDB**: A NoSQL document-oriented database for storing data.
- **Kafka**: A distributed event streaming platform used for building real-time data pipelines and streaming applications.
- **API Hitting**: Daemon thread hits an external API at an interval of 1 minute.
- **GET API with Search Functionality**: Provides a GET endpoint to search data stored in MongoDB.
- **POST API for API-KEY Registration**: Provides a POST endpoint to register key (few keys are already set by default).

## Requirements

- Python 3.7+
- MongoDB
- Kafka

## Installation

1. Clone this repository:

   ```bash
   git clone git@github.com:Bashar200/youtube-dashboard.git

2. Make sure Docker daemon or Docker app is running and run the following command
    ```bash
    docker-compose build --no-cache
3. Start docker containers
    ```bash
    docker-compose up

## Interaction

1. Access swagger docs at 
   ```bash
   http://localhost:8081/docs

2. Use GET API to perform necessary searches using swagger

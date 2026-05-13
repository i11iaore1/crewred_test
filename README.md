## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Environment Variables

Before starting the application, you need to configure the required environment variables. A template is provided in `.env.example`.

1. Copy the `.env.example` file to create your `.env` file:
2. Open the `.env` file and populate it with the necessary values. Here is a 
Example for .env:
PSQL_HOST=localhost
PSQL_EXT_PORT=5432
PSQL_PORT=$PSQL_EXT_PORT
PSQL_DB=db
PSQL_USER=user
PSQL_PASSWORD=password

## Building and Starting the Application

Once your `.env` file is set up, you can build and start the application using Docker Compose.

1. Build and start the containers with `docker compose up --build`

2. The application API will be available at:
   `http://localhost:8000`

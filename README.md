## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Environment Variables

Before starting the application, you need to configure the required environment variables. A template is provided in `.env.example`.

- Copy the `.env.example` file to create your `.env` file:
- Open the `.env` file and populate it with the necessary values. Here is an example for .env file content:
```
PSQL_HOST=localhost
PSQL_EXT_PORT=5432
PSQL_PORT=$PSQL_EXT_PORT
PSQL_DB=db
PSQL_USER=user
PSQL_PASSWORD=password
```
## Building and Starting the Application

- Build and start the containers with
   `docker compose up --build`

- The application API will be available at:
   `http://localhost:8000`

-  Automatic interactive API documentation (Swagger UI) can be found at:
   `http://localhost:8000/docs`

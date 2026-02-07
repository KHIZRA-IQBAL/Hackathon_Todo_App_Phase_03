# Todo App Backend

This directory contains the backend for the Todo Application, built with FastAPI.

## Setup

1.  **Install dependencies:**
    Make sure you have Python 3.9+ and pip installed. It's recommended to use a virtual environment.

    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure environment variables:**
    Create a `.env` file in this directory by copying the `.env.example` file.

    ```bash
    cp .env.example .env
    ```

    Update the `.env` file with your database connection string and a strong JWT secret.

## How to Run

To run the backend server for development, use the following command:

```bash
uvicorn backend.main:app --reload
```

The server will be available at `http://localhost:8000`.

## API Documentation

Once the server is running, you can access the interactive API documentation (Swagger UI) at:

[http://localhost:8000/docs](http://localhost:8000/docs)

This interface allows you to explore and test all the API endpoints.

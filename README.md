# Swamedia API Gateway

This project is a FastAPI-based API Gateway that provides authentication, rate limiting, and logging functionalities.

## Features

- JWT Authentication
- API Gateway Key Authentication
- Rate Limiting
- Request Logging
- Monitoring Endpoints

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/fast_api_python.git
    cd fast_api_python
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file based on the provided `.env.example` and configure your environment variables:
    ```sh
    cp .env.example .env
    ```

5. Run the application:
    ```sh
    uvicorn app.main:app --reload
    ```

## Usage

### Authentication

- **Login**: Obtain JWT access and refresh tokens.
    ```sh
    POST /login
    ```

- **Refresh Token**: Refresh the access token using a refresh token.
    ```sh
    POST /refresh
    ```

### Protected Endpoint

- Access a protected endpoint with valid API Gateway Key and JWT.
    ```sh
    GET /api/v1/protected
    ```

### Monitoring

- Get API usage statistics.
    ```sh
    GET /monitoring
    ```

## License

This project is licensed under the MIT License.

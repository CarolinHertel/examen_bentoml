# service.py
import bentoml
from bentoml.io import NumpyNdarray
from pydantic import BaseModel
from typing import Dict, List
import numpy as np
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import (
    AuthenticationBackend, AuthCredentials, SimpleUser, AuthenticationError
)
import jwt  # PyJWT library for decoding JWT tokens
from starlette.responses import JSONResponse

# Lade das Modell
scaler_ref = bentoml.sklearn.get("admission_model:23ua5ybkwkeif3wt")
scaler_runner = scaler_ref.to_runner()

# Definiere den BentoML Service
svc = bentoml.Service("scaler_service", runners=[scaler_runner])

# API-Input/Output definieren (hier: 2D-Numpy-Array, float32)
input_spec = NumpyNdarray(dtype="float32", shape=(-1, 7))  # 7 Features in deinem Fall
output_spec = NumpyNdarray()

# JWT Authentication Backend
class JWTAuthBackend(AuthenticationBackend):
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    async def authenticate(self, conn):
        # Extract the Authorization header
        auth_header = conn.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthenticationError("Invalid or missing Authorization header")

        token = auth_header.split(" ")[1]
        try:
            # Decode the JWT token
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return AuthCredentials(["authenticated"]), SimpleUser(payload["sub"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")

# Custom Authentication Middleware to return 401 on AuthenticationError
class CustomAuthenticationMiddleware(AuthenticationMiddleware):
    async def on_error(self, conn, exc):
        # Always return a JSON object with an "error" key
        print("CustomAuthenticationMiddleware triggered!")  # Add this line
        return JSONResponse({"error": str(exc)}, status_code=401)

# Add JWT Authentication Middleware
SECRET_KEY = "I_know_that_this _is_unsecure_but_I_don't_care"  # Replace with your actual secret key
svc.add_asgi_middleware(CustomAuthenticationMiddleware, backend=JWTAuthBackend(SECRET_KEY))

# Secure the predict API
@svc.api(input=input_spec, output=output_spec)
async def predict(input_data: np.ndarray) -> np.ndarray:
    # The user is authenticated at this point
    return await scaler_runner.predict.async_run(input_data)


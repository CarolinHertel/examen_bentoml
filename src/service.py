import bentoml
from bentoml.io import JSON
from pydantic import BaseModel
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
import os
from dotenv import load_dotenv
import numpy as np

# Load secret key from .env or hardcode for local testing
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET", "I_know_that_this _is_unsecure_but_I_don't_care")
ALGORITHM = "HS256"

# Dummy credentials
USERNAME = "admin"
PASSWORD = "4dm1N"

# Request schema
class AdmissionRequest(BaseModel):
    gre_score: float
    toefl_score: float
    university_rating: int
    sop: float
    lor: float
    cgpa: float
    research: int

class HTTPBearer401(HTTPBearer):
    async def __call__(self, request: Request):
        try:
            return await super().__call__(request)
        except HTTPException as exc:
            if exc.status_code == 403:
                raise HTTPException(status_code=401, detail="Not authenticated")
            raise
        
# Load model
model_ref = bentoml.sklearn.get("admission_model:latest")
model_runner = model_ref.to_runner()

svc = bentoml.Service("admission_service", runners=[model_runner])
app = FastAPI()
auth_scheme = HTTPBearer401()

# Auth token generator
def create_jwt_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Token validation dependency
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Login endpoint
@app.post("/login")
def login(request: dict):
    username = request.get("username")
    password = request.get("password")
    if username == USERNAME and password == PASSWORD:
        token = create_jwt_token(username)
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

def admission_request_to_numpy(admission_request: AdmissionRequest) -> np.ndarray:
    # Extract the values in the correct order and wrap in a list for a single sample
    features = [
        admission_request.gre_score,
        admission_request.toefl_score,
        admission_request.university_rating,
        admission_request.sop,
        admission_request.lor,
        admission_request.cgpa,
        admission_request.research
    ]
    return np.array([features], dtype=np.float32)  # shape: (1, 7)

# Predict endpoint
@app.post("/predict", dependencies=[Depends(verify_token)])
async def predict(input_data: AdmissionRequest):
    input_array = admission_request_to_numpy(input_data)
    prediction = await model_runner.predict.async_run(input_array)
    return {"chance_of_admit": round(prediction[0], 3)}

svc.mount_asgi_app(app)


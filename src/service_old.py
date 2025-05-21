import bentoml
from bentoml.io import JSON
from pydantic import BaseModel
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from dotenv import load_dotenv

# Load secret key from .env or hardcode for local testing
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET", "myjwtsecret")
ALGORITHM = "HS256"

# Dummy credentials
USERNAME = "admin"
PASSWORD = "4dm1N"

# Load model
model_ref = bentoml.sklearn.get("admission_model:latest")
model_runner = model_ref.to_runner()

svc = bentoml.Service("admission_service", runners=[model_runner])
app = FastAPI()
auth_scheme = HTTPBearer()

# Request schema
class AdmissionRequest(BaseModel):
    gre_score: float
    toefl_score: float
    university_rating: int
    sop: float
    lor: float
    cgpa: float
    research: int

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

# Predict endpoint
@app.post("/predict", dependencies=[Depends(verify_token)])
async def predict(input_data: AdmissionRequest):
    input_list = [[
        input_data.gre_score,
        input_data.toefl_score,
        input_data.university_rating,
        input_data.sop,
        input_data.lor,
        input_data.cgpa,
        input_data.research
    ]]
    prediction = await model_runner.predict.async_run(input_list)
    return {"chance_of_admit": round(prediction[0], 3)}

svc.mount_asgi_app(app)

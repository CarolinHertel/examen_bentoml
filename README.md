# 🎓 Student Admission Prediction API with BentoML

This project demonstrates a machine learning pipeline and API for predicting student admission chances. It uses BentoML to package, serve, and containerize the model, allowing easy deployment and testing. The API is secured using JWT authentication and includes automated unit tests.

---

## 📁 Project Structure

examen_bentoml/
├── data/
│ ├── raw/
│ └── admissions.zip
├── models/
├── src/
│ ├── train_model.py
│ ├── generate_token.py
│ └── service.py
├── tests/
│ └── test_api.py
├── requirements.txt
├── README.md


---

## 🚀 Getting Started

### 1. 📦 Environment Setup

```bash
# Optional: Unzip the dataset
unzip admissions.zip .

# Activate the virtual environment
source bentoml-env/bin/activate

# Navigate to the project directory
cd examen_bentoml

# Install dependencies
pip install -r requirements.txt

### 2. Build and Containerize with BentoML
cd src

python python train_model.py
# Build the Bento
bentoml build

# Containerize the Bento
bentoml containerize examen_bentoml:latest

# 🔍 Hint: If unsure about the Bento name, list all with:
bentoml list
```

### 3. Run the Docker Container

docker run --rm -d -p 3000:3000 examen_bentoml:1.0.0

# BentoML API will be available at `http://localhost:3000`

### 5. Run the API Tests

pytest tests/test_api.py

# Expected output:

=========================== test session starts ===========================
...
collected 3 items

tests/test_api.py ...                                              [100%]

============================ 3 passed in X.XXs ============================

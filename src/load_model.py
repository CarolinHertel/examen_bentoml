import transformers
import bentoml
from bentoml.models import BentoModel
import joblib


@bentoml.service(resources={"cpu": "200m", "memory": "512Mi"})
class MyService:
    # Define model reference at the class level
    # Load a model from the Model Store or BentoCloud
    sklearn_ref = bentoml.sklearn.get("admission_model:latest")

    def __init__(self):
        self.sklearn_ref = joblib.load(self.sklearn_ref.path_of("../model/scaler.pkl"))


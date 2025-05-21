import bentoml
import joblib

# Lade dein Modell
model = joblib.load("../models/scaler.pkl")

# Speichere es in BentoML
bento_model = bentoml.sklearn.save_model("scalar", model)
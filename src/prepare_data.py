import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os
import joblib

# Load data
df = pd.read_csv("../data/raw/admission.csv")

# Drop unnecessary columns:
df.drop(columns=["Serial No."], inplace=True, errors='ignore')

# Clean column names (remove trailing/leading spaces)
df.columns = df.columns.str.strip()

# Features and target
X = df.drop(columns=["Chance of Admit"])
y = df["Chance of Admit"]

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Save datasets
joblib.dump(X_train, "../data/processed/X_train.pkl")
joblib.dump(X_test, "../data/processed/X_test.pkl")
joblib.dump(y_train, "../data/processed/y_train.pkl")
joblib.dump(y_test, "../data/processed/y_test.pkl")

# Save scaler for later use in prediction API
joblib.dump(scaler, "../models/scaler.pkl")

print("✅ Data preparation complete. Files saved in data/processed/")
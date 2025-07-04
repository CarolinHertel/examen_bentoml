#!/bin/bash

# Exit immediately if a command fails
set -e

echo "🔄 Activating virtual environment..."
# virtualenv bentoml-env
# source bentoml-env/bin/activate
# cd examen_bentoml


echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🏗️  Navigating to source directory..."
cd src

echo "🚂 Training the model..."
python train_model.py
cd ..

echo "🔄 Build bentoml..."
bentoml build --version 1.0.0

echo "Containerize 📦the Bento..."
bentoml containerize admission_service:1.0.0

echo "Run the Docker Container"
docker run --rm -d -p 3000:3000 admission_service:1.0.0


echo "✅ All steps completed successfully!"
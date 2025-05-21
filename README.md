# Examen BentoML

Ce repertoire contient l'architecture basique afin de rendre l'évaluation pour l'examen BentoML.

## Deliverable 1: Instructions

### 1. Décompresser les fichiers et préparer l'environnement

```bash
# Décompresser les données si nécessaire
unzip data/admissions.zip -d data/raw

# Installer les dépendances Python
pip install -r requirements.txt

# Installer BentoML (si ce n'est pas déjà fait)
pip install bentoml
```

### 2. Construire et lancer l'API containerisée avec BentoML

```bash
# Construire l'image BentoML (remplacez 'admission_service:latest' par le nom de votre service si besoin)
bentoml build

# Containeriser l'API (crée une image Docker)
bentoml containerize admission_service:latest

# Lancer le conteneur Docker (remplacez le tag si besoin)
docker run -it --rm -p 3000:3000 admission_service:latest
```

### 3. Exécuter les tests unitaires

#### Avec unittest :
```bash
python -m unittest discover -s examen_bentoml/tests
```

#### Avec pytest (Deliverable 3) :
```bash
pytest examen_bentoml/tests
```

Tous les tests doivent retourner le statut **PASSED**.
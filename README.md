# M0-B1 — Maintenance - Alex

API Fast API permettant de prédire la criticité d'une machine pour la maintenance préventive.

---

## Fonctionnement de l'API

L'API exposée permet de: 
- Vérifier son état via l'endpoint `/health` (GET)
- Envoyer des caractéristiques machine via l'endpoint `/predict` (POST) pour obtenir une prédiction de criticité.
- D'obtenir la criticité prédite ainsi que des probabilités associées.

L'API enregistre un journal de logs via Loguru pour chaque requête reçue, est déployable via Docker et est testée via Pytest.

---

## 📁 Structure du repo

```
M0-B1-maintenance-Alex/
├── app/
│   ├── __init__.py
│   ├── main.py             ← FastAPI : /health (✅) + /predict (à compléter)
│   └── schemas.py          ← Pydantic : MachineInput, PredictionResponse
├── data/
│   ├── generate_dataset.py ← régénération du dataset (déjà exécuté)
│   └── maintenance_data.csv ← dataset synthétique 6 500 lignes
├── logs/
│   ├── api.log             ← logs de l'API 
├── model/
│   ├── train_baseline.py   ← entraînement (déjà exécuté)
│   └── model.joblib        ← modèle pré-entraîné ~6,6 Mo (chargé au démarrage)
├── tests/
│   ├── __init__.py
│   └── test_health.py      ← test pytest fonctionnel au clone (✅)
├── ressources/             ← 📚 mini-cours d'appui (lecture juste-à-temps)
│   ├── 01_FastAPI_essentiel.md
│   ├── 02_Docker_essentiel.md
│   ├── 03_Loguru_essentiel.md
│   ├── 04_Pytest_API_essentiel.md
│   ├── liens_officiels.md
│   └── README.md           ← ordre de mobilisation + objectifs
├── Dockerfile              ← squelette commenté à compléter
├── requirements.txt        ← dépendances figées
├── .gitignore
└── README.md (ce fichier — à compléter avec ta doc de service)
```

---

## ✏️ Prérequis

- Python 3.11+
- pip (ou pip3)
- virtualenv (ou venv)
- Docker (optionnel, pour la conteneurisation)
- `uvicorn` (installé via `pip install -r requirements.txt`)


---

## 🧭 Installation et lancement

1. Cloner le repo : `git clone <url> && cd M0-B1-maintenance-Alex`
2. Créer un environnement virtuel : `python -m venv .venv`
3. Activer l'environnement virtuel :
4. - Sur Linux/macOS : `source .venv/bin/activate`
   - Sur Windows : `.venv\Scripts\activate`
5. Installer les dépendances : `pip install -r requirements.txt`
6. Lancer le service : `uvicorn app.main:app --reload`
7. L'API est alors disponible sur `http://localhost:8000` et la documentation sur `http://localhost:8000/docs`.

(Optionnel)
1. Construire l'image Docker : `docker build -t maintenance-api .`
2. Lancer le conteneur : `docker run -p 8000:8000 maintenance-api`
3. L'API est alors disponible sur `http://localhost:8000` et la documentation sur `http://localhost:8000/docs`.



---

## 🎯 Test

Pour lancer les tests unitaires, exécuter la commande suivante dans le terminal :

```bash
pytest -q --disable-warnings  
```

---

## 📝 Misc.

Le Dockerfile inclut un Healthcheck pour vérifier l'état de l'API qui interroge l'endpoint `/health` toutes les 30 secondes.

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from typing import get_args
from app.schemas import TypeMachine
import pytest

valid_payload = {
    "type_machine": "compresseur",
    "age_machine_jours": 1500,
    "derniere_maintenance_jours": 45,
    "temperature_moyenne": 68.5,
    "vibration_moyenne": 3.2,
    "pression_moyenne": 7.8,
    "nb_incidents_3_mois": 2,
}


def test_predict_valid_payload_returns_200_and_valid_structure() -> None:
    """Un payload valide doit retourner 200 avec la structure attendue."""
    with TestClient(app) as client:
        response = client.post("/predict", json=valid_payload)

    assert response.status_code == 200

    body = response.json()

    assert "criticite" in body
    assert "probabilites" in body

    assert isinstance(body["criticite"], str)
    assert isinstance(body["probabilites"], dict)


def test_predict_invalid_machine_type_returns_422() -> None:
    """Un type_machine invalide doit retourner une erreur 422."""
    payload = valid_payload.copy()
    payload["type_machine"] = "machine_inconnue"

    with TestClient(app) as client:
        response = client.post("/predict", json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize("type_machine", get_args(TypeMachine))
def test_predict_accepts_all_machine_types(type_machine: str) -> None:
    payload = valid_payload.copy()
    payload["type_machine"] = type_machine

    with TestClient(app) as client:
        response = client.post("/predict", json=payload)

    assert response.status_code == 200

    body = response.json()

    assert "criticite" in body
    assert "probabilites" in body


def test_predict_returns_low() -> None:
    """L'endpoint /predict doit répondre avec une criticité estimée basse."""
    payload = {
        "type_machine": "compresseur",
        "age_machine_jours": 1500,
        "derniere_maintenance_jours": 45,
        "temperature_moyenne": 68.5,
        "vibration_moyenne": 3.2,
        "pression_moyenne": 7.8,
        "nb_incidents_3_mois": 2,
    }
    with TestClient(app) as client:
        response = client.post("/predict", json=payload)

        assert response.status_code == 200

        body = response.json()
        assert body["criticite"] == "basse"


def test_predict_returns_high() -> None:
    """L'endpoint /predict doit répondre avec une criticité estimée haute."""
    payload = {
        "type_machine": "compresseur",
        "age_machine_jours": 1500,
        "derniere_maintenance_jours": 365,
        "temperature_moyenne": 68.5,
        "vibration_moyenne": 10,
        "pression_moyenne": 7.8,
        "nb_incidents_3_mois": 215,
    }
    with TestClient(app) as client:
        response = client.post("/predict", json=payload)

        assert response.status_code == 200

        body = response.json()
        assert body["criticite"] == "haute"


def test_predict_returns_medium() -> None:
    """L'endpoint /predict doit répondre avec une criticité estimée moyenne."""
    payload = {
        "type_machine": "compresseur",
        "age_machine_jours": 1500,
        "derniere_maintenance_jours": 200,
        "temperature_moyenne": 68.5,
        "vibration_moyenne": 5,
        "pression_moyenne": 7.8,
        "nb_incidents_3_mois": 50,
    }
    with TestClient(app) as client:
        response = client.post("/predict", json=payload)

        assert response.status_code == 200

        body = response.json()
        assert body["criticite"] == "moyenne"

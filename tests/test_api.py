import joblib
from fastapi.testclient import TestClient

from src.app.main import app

client = TestClient(app)

GOOD = {
    "tenure_months": 5,
    "monthly_charges": 89.9,
    "contract": "month-to-month",
    "internet_service": "fiber",
    "support_calls": 3,
}


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_model_loads():
    model = joblib.load("models/model.joblib")
    assert hasattr(model, "predict_proba")


def test_predict_contract():
    r = client.post("/predict", json=GOOD)
    assert r.status_code == 200
    assert 0 <= r.json()["churn_probability"] <= 1


def test_missing_field():
    bad = dict(GOOD)
    del bad["tenure_months"]
    r = client.post("/predict", json=bad)
    assert r.status_code == 422


def test_wrong_type():
    bad = dict(GOOD)
    bad["support_calls"] = "many"
    r = client.post("/predict", json=bad)
    assert r.status_code == 422


def test_same_answer_twice():
    a = client.post("/predict", json=GOOD).json()["churn_probability"]
    b = client.post("/predict", json=GOOD).json()["churn_probability"]
    assert a == b

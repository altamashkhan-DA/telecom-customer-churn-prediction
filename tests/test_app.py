from app import app


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_prediction():
    client = app.test_client()
    payload = {
        "tenure": 12,
        "MonthlyCharges": 70,
        "TotalCharges": 840,
        "Contract": "Month-to-month",
        "InternetService": "Fiber optic",
        "PaymentMethod": "Electronic check",
        "OnlineSecurity": "No",
        "TechSupport": "No",
    }
    response = client.post("/predict", json=payload)
    result = response.get_json()
    assert response.status_code == 200
    assert result["prediction"] in {"Yes", "No"}
    assert 0 <= result["probability"] <= 100


def test_invalid_input():
    client = app.test_client()
    response = client.post("/predict", json={"tenure": "invalid"})
    assert response.status_code == 400

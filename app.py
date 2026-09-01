import os
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request

ROOT = Path(__file__).resolve().parent
MODEL = joblib.load(ROOT / "artifacts" / "churn_pipeline.joblib")

app = Flask(__name__)

FIELDS = {
    "tenure": {"default": 12, "min": 0, "max": 72},
    "MonthlyCharges": {"default": 70.0, "min": 0, "max": 200},
    "TotalCharges": {"default": 840.0, "min": 0, "max": 20000},
    "Contract": ["Month-to-month", "One year", "Two year"],
    "InternetService": ["DSL", "Fiber optic", "No"],
    "PaymentMethod": ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
    "OnlineSecurity": ["No", "Yes", "No internet service"],
    "TechSupport": ["No", "Yes", "No internet service"],
}


def validated_row(payload):
    row = {}
    for name in ("tenure", "MonthlyCharges", "TotalCharges"):
        try:
            value = float(payload[name])
        except (KeyError, TypeError, ValueError):
            raise ValueError(f"{name} must be a number")
        limits = FIELDS[name]
        if not limits["min"] <= value <= limits["max"]:
            raise ValueError(f"{name} must be between {limits['min']} and {limits['max']}")
        row[name] = value

    for name in ("Contract", "InternetService", "PaymentMethod", "OnlineSecurity", "TechSupport"):
        value = payload.get(name)
        if value not in FIELDS[name]:
            raise ValueError(f"Invalid {name}")
        row[name] = value

    if row["InternetService"] == "No":
        row["OnlineSecurity"] = "No internet service"
        row["TechSupport"] = "No internet service"
    return pd.DataFrame([row])


@app.get("/")
def index():
    return render_template("index.html", fields=FIELDS)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/predict")
def predict():
    try:
        row = validated_row(request.get_json(silent=True) or {})
        probability = float(MODEL.predict_proba(row)[0, 1])
        prediction = probability >= 0.50
        return jsonify({"prediction": "Yes" if prediction else "No", "probability": round(probability * 100, 1)})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)

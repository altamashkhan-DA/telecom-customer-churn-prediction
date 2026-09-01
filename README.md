# Telecom Customer Churn Prediction

An end-to-end machine-learning project that predicts whether a telecom customer is likely to churn and serves the result through a Flask web application.

**Author:** Mohammed Altamash Khan

## Project results

The final Logistic Regression pipeline was selected using leakage-safe five-fold cross-validation and evaluated once on an untouched 20% test set.

| Metric | Test result |
|---|---:|
| Accuracy | 73.3% |
| Precision | 49.8% |
| Recall | 77.5% |
| F1 score | 60.7% |
| ROC-AUC | 83.4% |

Recall is emphasized because the purpose of a churn model is to identify customers who may leave. The model detects approximately 78% of churners in the held-out test data, at the cost of more false-positive retention alerts.

## What was corrected

- Preprocessing now runs inside a scikit-learn `Pipeline`.
- Cross-validation uses original training rows; no duplicated records leak between folds.
- Class imbalance is handled with class weights instead of pre-CV oversampling.
- The model is trained on exactly the eight fields collected by the web app.
- The complete preprocessing-and-model pipeline is saved as one compact artifact.
- The Flask API validates numeric ranges and categorical values.

## Key findings

- Month-to-month customers show the highest churn rate.
- Churn is concentrated among customers with shorter tenure.
- Higher monthly charges are associated with churn.
- Service and contract patterns can help prioritize retention outreach.

These findings are associations in an IBM sample dataset and should not be interpreted as causal conclusions.

## Repository structure

```text
├── app.py
├── artifacts/
│   └── churn_pipeline.joblib
├── data/
│   └── Telco-Customer-Churn.csv
├── notebooks/
│   └── Telecom_Churn_Prediction.ipynb
├── static/
│   ├── app.js
│   └── style.css
├── templates/
│   └── index.html
├── tests/
│   └── test_app.py
├── requirements.txt
├── requirements-dev.txt
├── Procfile
├── LICENSE
└── README.md
```

## Run locally

```bash
cd telecom-customer-churn-prediction
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

Run the automated checks with `pytest -q`. GitHub Actions runs the same tests after every push.

## API example

Send a JSON `POST` request to `/predict` using the eight fields shown in the web form. The response contains `prediction` and churn `probability`.

## Dataset

The project uses the [IBM Telco Customer Churn sample dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn), containing 7,043 customer records. It is included for reproducibility and educational use.

## Limitations

- The dataset is a public sample, not recent production data.
- Model probability is a prioritization score, not proof that a customer will churn.
- Real deployment would require fresh data, cost-based threshold selection, monitoring and periodic retraining.

## License

Code is released under the MIT License. Dataset usage remains subject to its source terms.

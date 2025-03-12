from fastapi import FastAPI
from tasks import evaluate_credit

app = FastAPI(title="Credit Service API")

@app.get("/")
def read_root():
    return {"message": "Credit Service is running"}

@app.post("/credit/evaluate/")
def evaluate_credit_request(loan_data: dict):
    """ Permet de tester manuellement l'évaluation de crédit """
    evaluate_credit.delay(loan_data)
    return {"message": "✅ Évaluation de crédit en cours"}

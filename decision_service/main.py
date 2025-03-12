from fastapi import FastAPI
from tasks import evaluate_loan_decision

app = FastAPI(title="Decision Service API")

@app.get("/")
def read_root():
    return {"message": "Decision Service is running"}

@app.post("/decision/evaluate/")
def evaluate_decision_request(decision_data: dict):
    """ Permet de tester manuellement la prise de décision """
    evaluate_loan_decision.delay(decision_data)
    return {"message": "✅ Évaluation de la décision en cours"}

import logging
from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, HTTPException
from models import LoanRequest
from tasks import process_loan_request

app = FastAPI(title="Loan Service API")

@app.post("/loan/apply/")
def apply_loan(loan_request: LoanRequest):
    """ Endpoint pour soumettre une demande de prêt """
    loan_data = loan_request.dict()
    
    # Validation supplémentaire
    if loan_data["montant_demande"] > loan_data["valeur_bien"]:
        raise HTTPException(status_code=400, detail="Le montant demandé ne peut pas dépasser la valeur du bien.")

    # Exécution asynchrone avec Celery
    process_loan_request.delay(loan_data)

    return {
        "message": "✅ Demande de prêt reçue et envoyée en traitement.",
        "client_id": loan_request.client_id
    }

from fastapi import FastAPI
from tasks import evaluate_property

app = FastAPI(title="Property Service API")

@app.get("/")
def read_root():
    return {"message": "Property Service is running"}

@app.post("/property/evaluate/")
def evaluate_property_request(property_data: dict):
    """ Permet de tester manuellement l'évaluation du bien """
    evaluate_property.delay(property_data)
    return {"message": "✅ Évaluation du bien en cours"}

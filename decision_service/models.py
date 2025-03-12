from pydantic import BaseModel, Field

class DecisionRequest(BaseModel):
    client_id: int = Field(..., example=123)
    credit_score: int = Field(..., example=720)
    taux_endettement: float = Field(..., example=35.7)
    loan_to_value: float = Field(..., example=80.0)
    montant_demande: float = Field(..., example=200000)

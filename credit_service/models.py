from pydantic import BaseModel, Field

class CreditEvaluation(BaseModel):
    client_id: int = Field(..., example=123)
    revenu_annuel: float = Field(..., example=42000)
    credits_en_cours: float = Field(..., example=5000)
    situation_professionnelle: str = Field(..., example="CDI")
    montant_demande: float = Field(..., example=200000)
    duree: int = Field(..., example=20)

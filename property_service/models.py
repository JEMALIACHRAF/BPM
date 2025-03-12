from pydantic import BaseModel, Field

class PropertyEvaluation(BaseModel):
    client_id: int = Field(..., example=123)
    montant_demande: float = Field(..., example=200000)
    valeur_bien: float = Field(..., example=250000)

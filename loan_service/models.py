from pydantic import BaseModel, Field
from typing import Optional

class LoanRequest(BaseModel):
    client_id: int = Field(..., example=123)
    nom: str = Field(..., example="Jean Dupont")
    age: int = Field(..., ge=18, le=75, example=32)
    revenu_annuel: float = Field(..., example=42000)
    credits_en_cours: float = Field(..., example=5000)
    situation_professionnelle: str = Field(..., example="CDI")
    apport: float = Field(..., example=50000)
    valeur_bien: float = Field(..., example=250000)
    montant_demande: float = Field(..., example=200000)
    duree: int = Field(..., example=20)

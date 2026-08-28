from typing import Literal, Optional
from pydantic import BaseModel, Field

DRLabel = Literal["No DR", "Mild", "Moderate", "Severe", "Proliferative DR"]

class InitialDecision(BaseModel):
    case_id: str
    decision: DRLabel
    confidence: int = Field(ge=1, le=5)

class FinalDecision(BaseModel):
    case_id: str
    initial_decision: DRLabel
    initial_confidence: int = Field(ge=1, le=5)
    final_decision: DRLabel
    final_confidence: int = Field(ge=1, le=5)
    ai_prediction: Optional[DRLabel] = None
    ai_confidence: Optional[float] = Field(default=None, ge=0, le=1)
    explanation_opened: bool = False
    mode: Literal["no_ai", "ai_only", "ai_explanation"]

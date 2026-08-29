from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict

class FollowUpRiskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    age_band: Literal["0-17", "18-39", "40-59", "60+"]
    previous_missed_visits: int = Field(ge=0, le=20)
    lead_time_days: int = Field(ge=0, le=365)
    recommended_followup_days: int = Field(ge=1, le=730)
    visit_type: Literal["routine", "retina", "glaucoma", "post_op", "other"]
    contact_available: bool

class FollowUpRiskResponse(BaseModel):
    probability: float
    risk_band: Literal["low", "medium", "high"]
    model_status: Literal["trained_model", "research_baseline"]
    note: str

class InteractionEvent(BaseModel):
    study_id: str
    participant_id: str
    task_id: str
    event_type: Literal[
        "initial_decision",
        "ai_revealed",
        "explanation_opened",
        "final_decision",
        "followup_action_viewed"
    ]
    payload: dict = Field(default_factory=dict)
    timestamp_iso: Optional[str] = None

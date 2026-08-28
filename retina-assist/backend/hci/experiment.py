from enum import Enum
from uuid import uuid4
from datetime import datetime, timezone

class ExperimentMode(str, Enum):
    NO_AI = "no_ai"
    AI_ONLY = "ai_only"
    AI_EXPLANATION = "ai_explanation"

def new_case(mode: ExperimentMode) -> dict:
    return {
        "case_id": str(uuid4()),
        "mode": mode.value,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "initial_decision": None,
        "initial_confidence": None,
        "ai_revealed": False,
        "ai_prediction": None,
        "ai_confidence": None,
        "explanation_opened": False,
        "final_decision": None,
        "final_confidence": None,
        "ended_at": None,
    }

def summarize_reliance(case: dict) -> dict:
    initial = case.get("initial_decision")
    final = case.get("final_decision")
    ai = case.get("ai_prediction")
    changed = bool(initial and final and initial != final)
    changed_to_ai = bool(changed and ai and final == ai)
    return {"changed_decision": changed, "changed_to_ai": changed_to_ai}

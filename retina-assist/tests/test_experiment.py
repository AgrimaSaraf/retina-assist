from backend.hci.experiment import summarize_reliance

def test_change_to_ai():
    case = {
        "initial_decision": "Mild",
        "final_decision": "Moderate",
        "ai_prediction": "Moderate",
    }
    assert summarize_reliance(case) == {
        "changed_decision": True,
        "changed_to_ai": True,
    }

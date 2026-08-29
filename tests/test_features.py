from backend.followup.features import build_feature_frame

def test_features():
    f=build_feature_frame({
        "age_band":"40-59",
        "previous_missed_visits":1,
        "lead_time_days":14,
        "recommended_followup_days":30,
        "visit_type":"retina",
        "contact_available":True,
    })
    assert f.loc[0,"age_40-59"]==1
    assert f.loc[0,"visit_retina"]==1

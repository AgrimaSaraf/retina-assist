from backend.followup.record_linkage import fuzzy_match_deidentified
def test_match(): assert fuzzy_match_deidentified('participant alpha','participant  alpha').likely_match

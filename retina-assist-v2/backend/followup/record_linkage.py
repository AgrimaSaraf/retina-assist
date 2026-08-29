from dataclasses import dataclass
from rapidfuzz.fuzz import ratio

@dataclass(frozen=True)
class LinkageResult:
    score: float
    likely_match: bool

def normalize_token(value):
    if not value:
        return ""
    return " ".join(str(value).lower().strip().split())

def fuzzy_match_deidentified(
    left_alias,
    right_alias,
    left_age_band=None,
    right_age_band=None,
    threshold=90.0,
):
    # Public-repo demo for already de-identified aliases only.
    a = normalize_token(left_alias)
    b = normalize_token(right_alias)
    if not a or not b:
        return LinkageResult(0.0, False)
    score = float(ratio(a, b))
    if left_age_band and right_age_band and left_age_band != right_age_band:
        score -= 15.0
    score = max(0.0, min(100.0, score))
    return LinkageResult(score, score >= threshold)

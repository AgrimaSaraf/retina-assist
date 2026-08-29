from dataclasses import dataclass
from rapidfuzz.fuzz import ratio

@dataclass(frozen=True)
class LinkageResult:
    score: float
    likely_match: bool

def fuzzy_match_deidentified(a,b,threshold=90.0):
    a=' '.join(str(a).lower().strip().split())
    b=' '.join(str(b).lower().strip().split())
    score=float(ratio(a,b)) if a and b else 0.0
    return LinkageResult(score,score>=threshold)

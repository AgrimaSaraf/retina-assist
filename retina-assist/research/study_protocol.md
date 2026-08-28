# RetinaAssist HCI study protocol — draft

> Research planning document only. Obtain appropriate ethics/IRB/IEC review and clinical supervision before involving clinicians or patient-derived data.

## Goal
Study human-AI decision making in retinal fundus grading rather than merely measuring model accuracy.

## Conditions
1. **No AI** — participant grades the case independently.
2. **AI only** — participant records an initial judgment, then sees the model prediction.
3. **AI + explanation** — participant records an initial judgment, then sees prediction, confidence, and model-attention visualization.

## Core workflow
1. Present de-identified research case.
2. Capture initial grade and confidence.
3. Lock the initial response.
4. Reveal AI only when required by condition.
5. Capture explanation interaction.
6. Capture final grade and confidence.
7. Record decision time and whether the judgment changed.

## Safety
- Do not use RetinaAssist for clinical care.
- Do not expose patient identifiers to the prototype.
- Use approved, de-identified study material.
- Keep research data separate from application source code.
- Obtain required institutional/ethical approvals before a real study.

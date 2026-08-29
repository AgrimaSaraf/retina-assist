# RetinaAssist 2.0

**Human-centered AI research platform for retinal screening and ophthalmology follow-up workflows.**

RetinaAssist combines two related research directions:

1. **Human–AI retinal screening:** How should AI predictions, uncertainty, and explanations be shown to clinicians without encouraging inappropriate automation bias?
2. **Ophthalmology follow-up:** Can de-identified clinic workflow data help identify missed follow-up risk, and can a human-centered intervention improve the workflow?

> Research software only. RetinaAssist is not a medical device and must not be used for patient-care decisions.

## Architecture

```text
                     RETINAASSIST
                          |
                De-identified data
                          |
             +------------+------------+
             |                         |
      Retinal screening          Follow-up workflow
             |                         |
       Fundus image               Visit records
             |                         |
     Validated checkpoint        Data-quality checks
             |                         |
 Prediction + uncertainty       Baseline/risk model
             |                         |
       Explanation               Staff workflow
             +------------+------------+
                          |
                     HCI layer
                          |
               Research evaluation
```

## Repository

```text
backend/
  main.py
  schemas.py
  storage.py
  screening/
    model.py
    preprocessing.py
    inference.py
  followup/
    features.py
    record_linkage.py
    risk_model.py
analytics/
  baseline_analysis.py
  model_evaluation.py
data/
  README.md
  mock_visits.csv
  schema/visit_schema.json
frontend/
  app/
    page.tsx
    screening/page.tsx
    followup/page.tsx
    globals.css
  components/Nav.tsx
  lib/api.ts
research/
  hypotheses.md
  interview_guide.md
  workflow_observation_template.md
  protocol.md
  measures.md
  analysis_plan.md
scripts/
  generate_mock_data.py
  train_followup_model.py
tests/
```

## Run the backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Docs: `http://localhost:8000/docs`

## Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## Retinal model safety

Expected validated checkpoint:

```text
models/retinaassist_dr.pth
```

If it does not exist, `/screening/analyze` returns `503 MODEL_NOT_TRAINED`.

This is intentional. The codebase must not produce medical-looking predictions from random or ImageNet-only weights.

## Follow-up model

The repository contains a synthetic-data research sandbox. It lets the UI and pipeline run without pretending real clinic evidence exists.

```bash
python scripts/generate_mock_data.py
python scripts/train_followup_model.py
```

Any performance printed from this workflow is **synthetic-data performance only** and must not be reported as a clinical result.

## Data governance

Never commit:

- patient names
- phone numbers
- emails
- addresses
- medical-record numbers
- government identifiers
- unapproved retinal images
- identifiable free-text notes

Use a study-specific `research_id`.

Before clinic-derived data or a prospective patient/clinician study is used, obtain the appropriate clinic, privacy, ethical/IEC/IRB, consent, security, and research approvals for the actual design.

## Research sequence

```text
Observe clinic workflow
        ↓
Interview staff
        ↓
Measure the real problem
        ↓
Form research question
        ↓
Build minimum intervention
        ↓
Validate technically
        ↓
Run approved pilot
        ↓
Evaluate human + system outcomes
```

The project must be willing to conclude that a predictive model is unnecessary.

## Resume claims

Safe only after actually implemented:

> Built a human-centered AI research platform integrating retinal-screening infrastructure, FastAPI, a Next.js clinician interface, follow-up risk modeling, and reproducible HCI evaluation workflows.

Only after approved real data analysis:

> Analyzed de-identified ophthalmology workflow data across **[N] visits**, quantifying **[measured problem]** and evaluating predictors of follow-up non-adherence.

Only after a real evaluated intervention:

> Designed and evaluated **[intervention]**, measuring **[outcome]** across **[N] eligible encounters/users**.

Do not invent deployment status, sample sizes, accuracy, effect sizes, or patient outcomes.

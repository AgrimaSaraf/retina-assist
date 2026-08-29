# RetinaAssist

**Human-centered AI engineering and simulation platform for retinal screening and ophthalmology workflows.**

RetinaAssist is intentionally split into two layers:

```text
RETINAASSIST
│
├── ENGINEERING SYSTEM
│   ├── retinal screening pipeline
│   ├── follow-up risk pipeline
│   ├── FastAPI backend
│   ├── Next.js research interface
│   ├── fuzzy record linkage
│   ├── HCI interaction telemetry
│   └── evaluation utilities
│
└── SIMULATION / BENCHMARK
    ├── synthetic clinic cohort
    ├── synthetic appointments
    ├── simulated clinician decisions
    ├── simulated AI disagreement cases
    ├── simulated follow-up outcomes
    └── reproducible benchmark reports
```

> **Research software only. RetinaAssist is not a medical device and is not intended for patient-care decisions.**

No real patient outcomes, clinician outcomes, deployment results, or clinical effect sizes are claimed here.

## What I built

### Engineering system

- EfficientNet-B0 retinal-classification architecture with checkpoint-gated inference
- retinal-image preprocessing and confidence-aware prediction output
- FastAPI backend and Next.js/React interface
- follow-up feature engineering and logistic-regression risk-model scaffold
- fuzzy record linkage for de-identified aliases
- pre-AI/post-AI clinician interaction telemetry
- model/HCI evaluation utilities and automated tests

### Simulation / benchmark

- reproducible synthetic ophthalmology visit generator
- synthetic appointment and missed-follow-up histories
- simulated clinician judgments and AI predictions
- controlled clinician-AI disagreement cases
- simulated confidence changes and explanation interactions
- follow-up and HCI benchmark reports

All generated benchmark records contain `synthetic=1` and are not clinical evidence.

## Architecture

```text
                               RETINAASSIST
                                    |
                    +---------------+---------------+
                    |                               |
            ENGINEERING SYSTEM              SIMULATION / BENCHMARK
                    |                               |
          +---------+---------+             Synthetic clinic cohort
          |                   |                      |
  Retinal screening     Follow-up intelligence       |
          |                   |               Synthetic outcomes
    EfficientNet-B0      Feature engineering          |
          |                   |               Synthetic clinician
   Prediction output     Risk model scaffold          interactions
          +---------+---------+                      |
                    |                                |
                HCI layer <--------------------------+
                    |
       pre/post-AI decision logging
                    |
            benchmark evaluation
```

## Human-AI retinal screening

The architecture supports five DR classes: No DR, Mild, Moderate, Severe, and Proliferative DR.

```text
Fundus image → clinician initial decision → initial confidence → AI revealed
→ prediction/confidence → optional explanation → final decision → telemetry
```

The backend expects a checkpoint at `models/retinaassist_dr.pth`. If absent, `/screening/analyze` returns `503 MODEL_NOT_TRAINED` rather than producing an unvalidated medical-looking prediction.

## Follow-up intelligence

The follow-up layer works with operational features such as age band, visit type, previous missed visits, lead time, recommended follow-up interval, and contact-channel availability.

Model progression:

```text
prevalence baseline → simple rules → logistic regression → optional nonlinear model
```

The included model is trained only on synthetic data unless deliberately replaced with an appropriately governed dataset.

## Generate the simulation

```bash
python scripts/generate_synthetic_clinic.py
python scripts/simulate_human_ai_study.py
python scripts/train_followup_model.py
```

Generated files:

```text
data/synthetic/visits.csv
data/synthetic/appointments.csv
data/synthetic/human_ai_study.csv
models/followup_logistic.joblib
```

## Run benchmarks

```bash
python benchmarks/run_followup_benchmark.py
python benchmarks/run_hci_benchmark.py
```

Follow-up benchmark metrics include AUROC, average precision, Brier score, sensitivity, specificity, and PPV.

HCI simulation metrics include initial/final accuracy, switch rate, AI agreement, appropriate reliance, inappropriate reliance, confidence change, explanation-open rate, and decision time.

**These outputs describe a simulation, not real clinicians or patients.**

## Run backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

API docs: `http://localhost:8000/docs`

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

## Repository structure

```text
backend/
  main.py
  schemas.py
  storage.py
  screening/
  followup/
frontend/
  app/
  components/
  lib/
simulation/
  clinic_generator.py
  human_ai_generator.py
benchmarks/
  run_followup_benchmark.py
  run_hci_benchmark.py
analytics/
  followup_metrics.py
  hci_metrics.py
scripts/
  generate_synthetic_clinic.py
  simulate_human_ai_study.py
  train_followup_model.py
data/
  synthetic/
  schema/
research/
  hypotheses.md
  measures.md
  simulation_protocol.md
  real_world_validation_plan.md
models/
tests/
```

## Current status

**Implemented:** engineering scaffold, follow-up pipeline, checkpoint gating, API/UI, record linkage, synthetic clinic generator, synthetic human-AI generator, benchmarks, telemetry, tests.

**Not claimed:** clinical deployment, diagnostic efficacy, real patient outcomes, real clinician outcomes, reduced follow-up rates, prospective intervention effects, or real-world model validation.

## Future validation

```text
clinic workflow discovery
→ approved de-identified retrospective data
→ data-quality analysis
→ model validation
→ HCI refinement
→ appropriately approved clinician/patient evaluation
→ real-world outcome analysis
```

RetinaAssist is designed to benchmark the system before real-world testing, not to replace real-world validation.

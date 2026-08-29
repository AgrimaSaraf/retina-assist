# RetinaAssist 

**A human-centered AI research platform for retinal screening and ophthalmology workflow analysis.**

RetinaAssist is an end-to-end AI + HCI project I built to explore a broader question in healthcare AI:

> **How can AI support clinical decision-making and patient workflows without replacing human judgment?**

The project combines computer vision, machine learning, explainability, data engineering, backend development, frontend design, and HCI research methodology.

Rather than treating model accuracy as the entire problem, RetinaAssist is designed around the **human system surrounding the model**: how clinicians interpret AI predictions, when they trust or override them, how explanations affect decisions, and how operational clinic data can potentially be used to identify workflow problems such as missed follow-ups.

The project currently contains two connected research tracks:

1. **Human–AI retinal screening**
2. **Ophthalmology follow-up intelligence**

> **Research software only. RetinaAssist is not a medical device and is not intended for patient-care decisions.**

---

## What I Built

I designed RetinaAssist as a modular research platform consisting of:

* an **EfficientNet-B0 retinal-image classification architecture**
* retinal-image preprocessing pipelines
* infrastructure for model predictions and confidence scores
* explainability infrastructure for clinician-facing AI
* a **FastAPI backend**
* a **Next.js research interface**
* clinician interaction/event logging
* multiple HCI experimental conditions
* a de-identified ophthalmology visit-data schema
* follow-up feature-engineering pipelines
* a follow-up risk-modeling framework
* fuzzy record-linkage utilities for noisy de-identified records
* synthetic data generation for safe development
* baseline statistical analysis
* model evaluation infrastructure
* clinic workflow-discovery protocols
* HCI research hypotheses and measures
* a structured analysis plan for future real-world evaluation

The goal was to build not simply an image classifier, but the technical infrastructure required to **study AI as part of a real human clinical workflow**.

---

# System Architecture

```text
                         RETINAASSIST
                              |
                    De-identified data
                              |
              +---------------+---------------+
              |                               |
       RETINAL SCREENING              FOLLOW-UP WORKFLOW
              |                               |
         Fundus image                    Visit records
              |                               |
       Image preprocessing              Data cleaning
              |                               |
        EfficientNet-B0                Feature engineering
              |                               |
       Prediction scores               Risk modeling
              |                               |
         Uncertainty                   Record linkage
              |                               |
      AI explanation                  Workflow support
              |                               |
              +---------------+---------------+
                              |
                         HCI LAYER
                              |
                 Clinician-facing interface
                              |
                    Interaction logging
                              |
                     Research evaluation
```

---

# Research Track 1 — Human–AI Retinal Screening

The first part of RetinaAssist investigates how clinicians interact with AI-assisted retinal screening.

The system architecture supports a five-class diabetic-retinopathy classification task:

| Class | Retinopathy Level |
| ----- | ----------------- |
| 0     | No DR             |
| 1     | Mild              |
| 2     | Moderate          |
| 3     | Severe            |
| 4     | Proliferative DR  |

I implemented the retinal-model infrastructure using **PyTorch and EfficientNet-B0**.

The pipeline is structured as:

```text
Fundus image
      ↓
Image preprocessing
      ↓
EfficientNet-B0
      ↓
Class probabilities
      ↓
Predicted DR class
      ↓
Confidence / uncertainty
      ↓
Clinician interface
```

The architecture deliberately separates **model inference from clinical interpretation**.

RetinaAssist does not assume that an AI prediction should automatically become the final clinical decision.

Instead, the system is designed to study what happens when a clinician sees AI-generated information.

---

# Human–AI Interaction Design

One of the central ideas behind RetinaAssist is that the **presentation of AI may matter almost as much as the model itself**.

I therefore structured the research interface around three experimental conditions:

### Condition A — No AI

The clinician evaluates the retinal image independently.

### Condition B — AI Prediction

The clinician makes an initial judgment and is subsequently shown the AI prediction and confidence.

### Condition C — AI + Explanation

The clinician receives the prediction, confidence information, and an explanation layer.

This allows the system to investigate questions such as:

* Does AI change the clinician's original decision?
* When do clinicians appropriately override AI?
* When do clinicians follow an incorrect AI prediction?
* Does an explanation increase trust?
* Can explanations accidentally increase automation bias?
* How does clinician confidence change after seeing AI?
* How does AI affect decision time?

---

# Pre-AI and Post-AI Decisions

The interface is structured to preserve the clinician's **independent judgment before AI exposure**.

```text
Retinal image
      ↓
Clinician initial decision
      ↓
Initial confidence
      ↓
AI revealed
      ↓
Prediction / confidence / explanation
      ↓
Clinician final decision
      ↓
Final confidence
```

This makes it possible to study **human–AI reliance**, rather than merely measuring whether the human and model agree.

The event-logging layer can capture interactions such as:

```text
initial_decision
ai_revealed
explanation_opened
final_decision
```

These events provide the infrastructure for later analysis of clinician behavior.

---

# Research Track 2 — Ophthalmology Follow-Up Intelligence

I extended RetinaAssist beyond image classification to investigate another part of ophthalmology care:

> **What happens after the patient leaves the examination room?**

Patients may be advised to return after a particular period, but operational friction can potentially lead to delayed or missed follow-ups.

I therefore built a second pipeline for studying ophthalmology follow-up workflows.

```text
Visit records
      ↓
De-identification
      ↓
Data-quality checks
      ↓
Feature engineering
      ↓
Follow-up dataset
      ↓
Baseline analysis
      ↓
Risk modeling
      ↓
Human-centered workflow
```

The purpose of this component is not to assume that AI will solve follow-up problems.

Instead, it provides the infrastructure to first **measure whether the problem exists**, understand its characteristics, and then test whether prediction or workflow redesign adds useful value.

---

# De-identified Visit Data

I created a structured visit-data schema using research-specific identifiers rather than direct patient identifiers.

Example variables include:

```text
research_id
age_band
visit_type
previous_missed_visits
lead_time_days
recommended_followup_days
contact_available
followup_recommended
missed_followup
days_late
```

The public repository contains **synthetic records only**.

The synthetic dataset allows the engineering pipeline, analytics scripts, API, and interface to be developed without exposing real patient information.

---

# Follow-Up Feature Engineering

I built a feature-engineering layer that transforms visit information into model-ready variables.

Current features include:

* age band
* previous missed visits
* appointment lead time
* recommended follow-up interval
* visit type
* availability of a contact channel

The architecture makes it possible to compare simple operational rules with statistical or machine-learning models.

The intended progression is:

```text
Prevalence baseline
        ↓
Simple operational rules
        ↓
Logistic regression
        ↓
Optional nonlinear models
```

A more complicated model should only be used if it demonstrates meaningful value over simpler approaches.

---

# Follow-Up Risk Modeling

I implemented a baseline **logistic-regression modeling pipeline** for follow-up research.

The pipeline includes:

* feature generation
* train/test splitting
* model training
* probability estimation
* risk-band generation
* model artifact storage
* evaluation scripts

The repository also contains a transparent engineering baseline so that the complete application can run without pretending that a clinic-trained model already exists.

Any model trained using the included synthetic dataset is strictly a **software-development artifact**, not a clinically validated model.

---

# Fuzzy Record Linkage

Real-world administrative and clinical datasets are often messy.

Records may contain inconsistent spellings, duplicated entries, or slightly different representations of the same entity.

I therefore implemented a fuzzy record-linkage utility using **RapidFuzz**.

Conceptually:

```text
Record A
"participant alpha"

Record B
"participant  alpha"

        ↓

String normalization
        ↓
Fuzzy similarity
        ↓
Matching score
```

The public implementation operates on **de-identified aliases only**.

Any linkage involving real identifiers would require separate privacy controls and validation because incorrect record merging can itself introduce serious data-quality problems.

---

# Analytics

I created an analytics layer for studying follow-up behavior.

The baseline-analysis pipeline can calculate metrics such as:

```text
Total visits
Eligible follow-up visits
Missed follow-up rate
Median days late
Contact availability
```

The model-evaluation infrastructure includes:

* AUROC
* average precision
* Brier score
* classification performance
* calibration-oriented evaluation

This is important because a healthcare prediction system cannot be evaluated using accuracy alone.

A model can discriminate between higher- and lower-risk cases while still producing badly calibrated probabilities.

---

# Synthetic Data Pipeline

Real patient data is not required to develop the software architecture.

I therefore built a reproducible synthetic-data generator that creates mock ophthalmology visit records.

```bash
python scripts/generate_mock_data.py
```

The resulting dataset can be used to test:

* data loading
* feature engineering
* analytics
* model training
* API endpoints
* frontend workflows

The generated records are entirely synthetic and are **not presented as clinic observations or clinical evidence**.

---

# Backend

The backend is built using **FastAPI**.

Core endpoints include:

```text
GET  /health

POST /screening/analyze

POST /followup/risk

POST /research/event
```

The backend connects:

```text
Frontend
   ↓
FastAPI
   ↓
Screening / Follow-up services
   ↓
Models
   ↓
Research logging
```

---

# Frontend

I built the research interface using **Next.js and React**.

The interface contains two primary research environments:

### Retinal Screening

Used for human–AI retinal-screening experiments.

### Follow-Up Workflow

Used for experimenting with de-identified visit characteristics and the follow-up modeling pipeline.

The interface deliberately labels outputs as **research outputs** rather than clinical recommendations.

---

# Retinal Model Safety

The screening backend expects a validated retinal checkpoint at:

```text
models/retinaassist_dr.pth
```

If the checkpoint is unavailable, the API returns:

```text
503 MODEL_NOT_TRAINED
```

rather than generating a prediction from untrained weights.

This behavior is intentional.

An untrained neural network can still generate convincing-looking probabilities. In a healthcare interface, presenting those numbers would create a misleading impression that the model has medical meaning.

RetinaAssist therefore fails explicitly rather than fabricating a prediction.

---

# Research and HCI Layer

In addition to the software system, I created a research framework for investigating the system in a real ophthalmology environment.

The `research/` directory contains:

```text
hypotheses.md
interview_guide.md
workflow_observation_template.md
protocol.md
measures.md
analysis_plan.md
```

These documents structure the project around a research process rather than starting with a predetermined AI solution.

---

# Clinic Workflow Discovery

The first real-world stage of the project is designed around observing how an ophthalmology clinic actually operates.

The workflow can be mapped as:

```text
Patient arrival
      ↓
Registration
      ↓
Waiting
      ↓
Eye examination
      ↓
Imaging
      ↓
Clinician review
      ↓
Diagnosis / counselling
      ↓
Follow-up recommendation
      ↓
Scheduling
      ↓
Patient returns / does not return
```

The workflow-discovery framework records:

* actors involved
* systems/tools used
* approximate task time
* repeated work
* information bottlenecks
* patient friction
* potential measurement strategies

The purpose is to identify the **actual problem before deciding that machine learning is necessary**.

---

# Research Questions

## Human–AI Screening

RetinaAssist is designed to investigate questions such as:

> How does AI assistance change clinician retinal-screening decisions?

> Does showing an AI explanation affect appropriate reliance?

> What happens when the AI prediction conflicts with the clinician's initial judgment?

> Does explanation help clinicians detect incorrect AI predictions, or can it increase automation bias?

---

## Follow-Up Workflow

The second research track investigates:

> What proportion of eligible ophthalmology visits fail to complete recommended follow-up?

> Which routinely available variables are associated with missed follow-up?

> Can a simple predictive model outperform operational rules?

> Can a human-centered digital workflow improve the follow-up process?

These are research questions rather than predetermined conclusions.

---

# Evaluation Framework

RetinaAssist is designed to evaluate three different levels of system performance.

## 1. Model Performance

```text
AUROC
Average precision
Sensitivity
Specificity
PPV
Calibration
Brier score
```

## 2. Human–AI Performance

```text
Initial clinician decision
Final clinician decision
Confidence change
Agreement with reference standard
Appropriate reliance
Inappropriate reliance
Decision time
Explanation usage
```

## 3. Workflow Performance

```text
Follow-up completion
Days late
No-show rate
Staff time
Manual workflow steps
Task completion
Usability
Perceived workload
```

The distinction matters because a model can perform well statistically while still making the overall human system worse.

---

# Repository Structure

```text
retina-assist/

├── backend/
│   ├── main.py
│   ├── schemas.py
│   ├── storage.py
│   │
│   ├── screening/
│   │   ├── model.py
│   │   ├── preprocessing.py
│   │   └── inference.py
│   │
│   └── followup/
│       ├── features.py
│       ├── record_linkage.py
│       └── risk_model.py
│
├── analytics/
│   ├── baseline_analysis.py
│   └── model_evaluation.py
│
├── data/
│   ├── README.md
│   ├── mock_visits.csv
│   └── schema/
│       └── visit_schema.json
│
├── frontend/
│   ├── app/
│   │   ├── screening/
│   │   ├── followup/
│   │   └── page.tsx
│   ├── components/
│   └── lib/
│
├── models/
│
├── research/
│   ├── hypotheses.md
│   ├── interview_guide.md
│   ├── workflow_observation_template.md
│   ├── protocol.md
│   ├── measures.md
│   └── analysis_plan.md
│
├── scripts/
│   ├── generate_mock_data.py
│   └── train_followup_model.py
│
├── tests/
│
├── requirements.txt
└── README.md
```

---

# Running RetinaAssist

## Backend

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn backend.main:app --reload
```

API documentation:

```text
http://localhost:8000/docs
```

---

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

---

# Generate Research Mock Data

```bash
python scripts/generate_mock_data.py
```

This generates synthetic ophthalmology visit records for testing the data and modeling pipeline.

---

# Train the Follow-Up Research Model

```bash
python scripts/train_followup_model.py
```

The resulting model is trained entirely on synthetic data unless explicitly replaced with an appropriately governed real-world research dataset.

Its performance therefore **must not be interpreted as clinical performance**.

---

# Technology Stack

**Machine Learning**

* Python
* PyTorch
* torchvision
* EfficientNet-B0
* scikit-learn
* logistic regression

**Data**

* pandas
* NumPy
* RapidFuzz
* JSON Schema

**Backend**

* FastAPI
* Pydantic
* Uvicorn

**Frontend**

* Next.js
* React
* TypeScript

**Research / HCI**

* human–AI decision logging
* experimental-condition design
* workflow observation
* usability evaluation
* model calibration
* appropriate-reliance analysis

---

# Data Privacy

The GitHub repository does **not** contain real patient data.

Direct patient identifiers should never be committed, including:

* names
* phone numbers
* email addresses
* home addresses
* medical-record numbers
* government identifiers
* identifiable clinical notes
* unapproved clinical images

Any future work involving clinic-derived data should use an appropriately governed, minimum-necessary, de-identified or pseudonymized dataset and follow the applicable institutional, ethical, privacy, security, consent, and clinical requirements.

---

# Current Status

### Implemented

* RetinaAssist system architecture
* EfficientNet-B0 retinal-model architecture
* image preprocessing
* retinal inference infrastructure
* model-checkpoint safety mechanism
* FastAPI backend
* Next.js frontend
* screening research interface
* follow-up research interface
* de-identified visit-data schema
* synthetic visit-data generator
* follow-up feature engineering
* logistic-regression training pipeline
* fuzzy record-linkage utility
* baseline analytics
* model-evaluation infrastructure
* research interaction logging
* HCI hypotheses
* clinic interview guide
* workflow-observation framework
* research protocol scaffold
* analysis plan
* automated API/feature tests

### Next Research Phase

```text
Clinic workflow observation
        ↓
Stakeholder interviews
        ↓
Problem quantification
        ↓
Approved de-identified retrospective analysis
        ↓
Model validation
        ↓
HCI prototype iteration
        ↓
Appropriately approved prospective evaluation
```

---

# Why I Built RetinaAssist

I wanted to explore healthcare AI beyond the standard:

```text
dataset → model → accuracy
```

Real-world AI systems operate inside human organizations.

A useful healthcare AI system therefore needs more than a high-performing neural network.

It needs to answer questions about:

```text
Who uses the model?

When do they see its prediction?

How is uncertainty communicated?

When should they trust it?

When should they override it?

Does the interface change their behavior?

Does the technology actually improve the workflow?

What happens when the AI is wrong?
```

RetinaAssist is my attempt to explore those questions by combining **machine learning, computer vision, software engineering, data systems, and human-computer interaction in one research platform.**

The long-term goal is not simply to make AI predict retinal disease.

It is to understand how AI can be designed to **work responsibly with humans in real clinical environments.**

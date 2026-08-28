# RetinaAssist

**Human-centered AI for retinal screening research**

RetinaAssist is a research prototype combining computer vision with Human–AI Interaction (HCI). The intended research question is not simply *“Can a model classify a retinal image?”* but *“How should AI predictions, uncertainty, and explanations be presented so clinicians can use them without inappropriate automation bias?”*

## What is implemented

- EfficientNet-B0 5-class DR model architecture
- Safe checkpoint loading: no retinal checkpoint = no prediction
- Fundus image preprocessing
- Engineering-only image-quality heuristic
- Grad-CAM model-attention visualization
- FastAPI inference API
- Next.js clinician-facing dashboard
- Three HCI study conditions
- Initial/final clinician decision workflow
- Interaction-event instrumentation
- Draft HCI research questions, measures, protocol, and analysis plan
- Basic tests

## Deliberately not included

`models/retinaassist_dr.pth`

A retinal classifier must be trained and independently evaluated before the application can return retinal predictions. RetinaAssist deliberately refuses to generate predictions from random or ImageNet-only weights.

## DR labels

0. No DR
1. Mild
2. Moderate
3. Severe
4. Proliferative DR

## Architecture

```text
Fundus image
    |
    +--> image-quality heuristic
    |
    v
EfficientNet-B0 + validated retinal checkpoint
    |
    +--> DR severity probabilities
    |
    +--> Grad-CAM
    |
    v
FastAPI
    |
    v
Clinician HCI interface
    |
    +--> initial judgment
    +--> AI reveal (condition dependent)
    +--> explanation interaction
    +--> final judgment
    |
    v
De-identified research events
```

## Backend

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

API docs are available at `/docs`.

Without a retinal checkpoint, `/health` works and `/analyze` returns `503 MODEL_NOT_TRAINED`. This is intentional.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend defaults to `http://localhost:8000` for the API. Set `NEXT_PUBLIC_API_URL` for deployment.

## Model checkpoint

After training and validation, save the model state dictionary to:

```text
models/retinaassist_dr.pth
```

The architecture expects five outputs corresponding to the labels above.

## HCI design

The UI supports:

- **A · No AI**
- **B · AI prediction**
- **C · AI + explanation**

The research workflow captures an independent clinician judgment before AI reveal, allowing study of appropriate reliance and automation bias.

See `research/`.

## Safety and research boundaries

RetinaAssist is **not a medical device and not a diagnostic system**. It must not be used to make patient-care decisions. Do not place PHI or patient identifiers in this repository or its local JSONL event log.

Before using clinic-derived images or conducting a clinician/patient study, obtain the appropriate institutional, ethical, privacy, consent, and clinical approvals.

## Next engineering milestones

1. Train and validate the retinal checkpoint.
2. Add held-out/external validation.
3. Replace the quality heuristic with a validated image-quality model.
4. Calibrate model probabilities on validation data.
5. Add secure study authentication and approved research storage.
6. Implement randomized study-condition assignment.
7. Add timing and interaction telemetry.
8. Conduct a supervised pilot before a formal HCI study.

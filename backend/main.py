from io import BytesIO

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError

from backend.ml.inference import service
from backend.ml.quality import assess_image_quality
from backend.hci.experiment import ExperimentMode, new_case, summarize_reliance
from backend.hci.logging import log_event
from backend.schemas import InitialDecision, FinalDecision

app = FastAPI(
    title="RetinaAssist API",
    version="0.1.0",
    description="Research prototype for human-centered retinal AI."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def read_image(file: UploadFile) -> Image.Image:
    if file.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(415, "Please provide a JPEG or PNG retinal image.")
    raw = await file.read()
    if len(raw) > 20 * 1024 * 1024:
        raise HTTPException(413, "Image exceeds 20 MB.")
    try:
        return Image.open(BytesIO(raw)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(400, "The uploaded file is not a valid image.")

@app.get("/health")
def health():
    return {"api": "ok", "model": service.status()}

@app.post("/quality")
async def quality(file: UploadFile):
    image = await read_image(file)
    return assess_image_quality(image)

@app.post("/analyze")
async def analyze(file: UploadFile):
    image = await read_image(file)
    if not service.ready:
        raise HTTPException(
            503,
            detail={
                "code": "MODEL_NOT_TRAINED",
                "message": (
                    "The RetinaAssist retinal checkpoint has not been installed. "
                    "The API will not generate fake medical predictions."
                ),
                "model": service.status(),
            },
        )
    return service.analyze(image)

@app.post("/study/cases/{mode}")
def create_study_case(mode: ExperimentMode):
    case = new_case(mode)
    log_event({"event": "case_created", **case})
    return case

@app.post("/study/initial")
def record_initial(payload: InitialDecision):
    event = {"event": "initial_decision", **payload.model_dump()}
    log_event(event)
    return {"saved": True}

@app.post("/study/final")
def record_final(payload: FinalDecision):
    case = payload.model_dump()
    metrics = summarize_reliance(case)
    log_event({"event": "final_decision", **case, **metrics})
    return {"saved": True, "reliance": metrics}

import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
from .schemas import FollowUpRiskRequest, FollowUpRiskResponse, InteractionEvent
from .followup.risk_model import FollowUpRiskModel
from .screening.inference import ScreeningEngine
from .storage import write_event

app = FastAPI(title="RetinaAssist Research API", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

followup_model = FollowUpRiskModel()
screening_engine = ScreeningEngine()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "retinal_model_ready": screening_engine.ready,
        "research_only": True,
    }

@app.post("/followup/risk", response_model=FollowUpRiskResponse)
def followup_risk(request: FollowUpRiskRequest):
    return followup_model.predict(request.model_dump())

@app.post("/research/event")
def research_event(event: InteractionEvent):
    write_event(event.model_dump())
    return {"saved": True}

@app.post("/screening/analyze")
async def screening_analyze(file: UploadFile = File(...)):
    if not screening_engine.ready:
        raise HTTPException(
            503,
            detail={
                "code": "MODEL_NOT_TRAINED",
                "message": "No validated retinal checkpoint is available."
            },
        )
    raw = await file.read()
    if len(raw) > 10 * 1024 * 1024:
        raise HTTPException(413, "Image exceeds 10 MB.")
    try:
        image = Image.open(io.BytesIO(raw))
        image.load()
    except UnidentifiedImageError:
        raise HTTPException(400, "Invalid image.")
    return screening_engine.analyze(image)

import io
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
from .schemas import FollowUpRiskRequest, FollowUpRiskResponse, InteractionEvent
from .followup.risk_model import FollowUpRiskModel
from .screening.inference import ScreeningEngine
from .storage import write_event
app=FastAPI(title='RetinaAssist Research API',version='3.0.0')
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:3000'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
followup=FollowUpRiskModel(); screening=ScreeningEngine()
@app.get('/health')
def health(): return {'status':'ok','retinal_model_ready':screening.ready,'research_only':True,'simulation_supported':True}
@app.post('/followup/risk',response_model=FollowUpRiskResponse)
def risk(req:FollowUpRiskRequest): return followup.predict(req.model_dump())
@app.post('/research/event')
def event(e:InteractionEvent): write_event(e.model_dump()); return {'saved':True}
@app.post('/screening/analyze')
async def analyze(file:UploadFile=File(...)):
    if not screening.ready: raise HTTPException(503,detail={'code':'MODEL_NOT_TRAINED','message':'No validated retinal checkpoint is available.'})
    raw=await file.read()
    try: image=Image.open(io.BytesIO(raw)); image.load()
    except UnidentifiedImageError: raise HTTPException(400,'Invalid image')
    return screening.analyze(image)

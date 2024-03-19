from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import ffmpeg
from pydantic import BaseModel
from pydub import AudioSegment
from services import audio_to_text
from db import migration
import io
import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
templates = Jinja2Templates(directory="templates")
migration.migrate()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Allow requests from all origins
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
        )

@app.get("/transcribe")
async def transcribe(request: Request):
    """
    Transcribe an audio file
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/transcribe")
async def transcribe(request: Request, audio_file: UploadFile = File(...)):
    """
    Transcribe an audio file
    """
    content_length = int(request.headers.get("content-length"))
    if content_length > (25 * 1024 * 1024):  # Convert MB to bytes
        raise HTTPException(status_code=413, detail="File size exceeds 25MB limit")

    logger = logging.getLogger()

    logger.info(" content length: {}".format(content_length))
    logger.info(" content type: {}".format(audio_file.content_type))
    logger.info(" file name: {}".format(audio_file.filename))
    if audio_file.content_type == 'audio/mpeg':
        audio = AudioSegment.from_file(audio_file.file, format="mp3")  # when picking up files from local
    elif audio_file.content_type == 'audio/webm; codecs=opus':
        audio = AudioSegment.from_file(audio_file.file, codec="opus")   # when recording directly from browser
    else:
        raise HTTPException(status_code=415, detail="Unsupported media type")

    buffer = io.BytesIO()
    buffer.name = audio_file.filename
    audio.export(buffer, format="mp3")

    transcript = audio_to_text.audio_to_text(audio_file.filename, buffer)

    return JSONResponse(content={"transcript": transcript}, headers={"Content-Type": "application/json; charset=utf-8"})
    #return templates.TemplateResponse("index.html", {"request": request, "transcript": transcript})

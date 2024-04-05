import io
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db import migration
from app.routers import transcribe, admin, authentication

app = FastAPI()

logging.basicConfig(level=logging.INFO)
migration.migrate()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Allow requests from all origins
app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
        )

# Include routers
# TODO: missing tests for admin and authentication routers, missing a couple of pieces here and there
#app.include_router(admin.router)
#app.include_router(authentication.router)
app.include_router(transcribe.router)

from fastapi import APIRouter
from fastapi import HTTPException, Request, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
from jose import jwt

from app.db import users_repo

import os
import logging

TOKEN_EXPIRATION_MINUTES = os.environ.get("TOKEN_EXPIRATION_MINUTES", 30)
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PWD = os.environ.get("ADMIN_PWD", "admin")
SECRET_KEY = os.environ.get("SECRET_KEY", "some_secret_key")

router = APIRouter()
logger = logging.getLogger()
templates = Jinja2Templates(directory="app/templates")

# Generate JWT token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

# Define a function to authenticate users and generate JWT token
def authenticate_user(username: str, password: str):
    if username == ADMIN_USERNAME and password == ADMIN_PWD:
        return {"username": "admin", "role": "admin"}

    user = users_repo.find(username)
    logger.info("user {}".format(user))
    if not user or user["password"] != users_repo.hashPassword(password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    if not user["approved"]:
        raise HTTPException(status_code=403, detail="User not approved by admin")
    return {"username": user["username"], "role": "user"}

# Sign-up endpoint
@router.post("/signup")
async def sign_up(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        logger.info("tryingo to create user")
        users_repo.create(form_data.username, form_data.password)
        # TODO: handle username already exits
    except:
        raise HTTPException(status_code=400, detail="Username already exists")

    return {"message": "Sign-up successful, awaiting admin approval"}

# GET endpoint for the signup form
@router.get("/signup")
async def get_signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# GET endpoint for the login form
@router.get("/login")
async def get_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Login endpoint
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    logger.info("user {}".format(user))
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )
    #return Response(status_code=302, headers={"Location": "/transcribe", "Authorization": "Bearer {}".format(access_token), "Access-Control-Expose-Headers": "Authorization"})
    return Response(status_code=200, headers={"Location": "/transcribe", "Authorization": "Bearer {}".format(access_token), "Access-Control-Expose-Headers": "Authorization"})


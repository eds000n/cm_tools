import os

from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, UploadFile, File, Request, Depends, status, Response
from fastapi.security import OAuth2PasswordBearer
from app.db import users_repo
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = os.environ.get("SECRET_KEY")

async def get_admin_role(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    if payload['role'] != 'admin':
        raise HTTPException(status_code=403)

router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(get_admin_role)],
)

# Define an endpoint for the admin to approve a user
@router.put("/approve/{username}")
async def approve_user(username: str):
    not_approved_users = users_repo.listNotApproved()
    if username not in not_approved_users:
        raise HTTPException(status_code=404, detail="User not found")
    users_repo.setApproved(username)
    return {"message": f"User {username} has been approved"}

# Define an endpoint for the admin to reject a user
@router.put("/reject/{username}")
async def reject_user(username: str):
    #not_approved_users = users_repo.listNotApproved()
    #if username not in not_approved_users:
    #    raise HTTPException(status_code=404, detail="User not found")
    users_repo.removeUser(username)
    return {"message": f"User {username} has been rejected and removed"}


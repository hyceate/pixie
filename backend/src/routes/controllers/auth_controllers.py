from fastapi import Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from ...db import redis_client
from ...config import SessionLocal
from ...models import User
import os
import uuid
import json

secret = os.getenv('SECRET_KEY', 'your-secret-key')
SESSION_COOKIE_NAME = 'ssid'
SESSION_EXPIRATION_MINUTES = 60 # 1 minute
EXPIRES = SESSION_EXPIRATION_MINUTES * 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class RegisterRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

async def create_user(username: str, display_name: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    new_user = User(username=username, display_name=display_name)
    new_user.set_password(password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def store_token(token_id: str, token: str, expires_in: int, user_id: uuid.UUID):
    user_id_str = str(user_id)
    token_data = {
        "token": token,
        "user_id": user_id_str
    }
    token_data_str = json.dumps(token_data)
    redis_client.setex(f"session:{token_id}", expires_in, token_data_str)

def delete_token(token_id: str):
    redis_client.delete(f"session:{token_id}")

def get_token_data(token_id: str):
    token_data_str = redis_client.get(f"session:{token_id}")
    if token_data_str:
        print(f"Token Data Retrieved: {token_data_str}")
        return json.loads(token_data_str)
    print("No Token Data Found")
    return None

async def get_current_user(request: Request, db: Session = Depends(SessionLocal)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = request.cookies.get("ssid")
    if not token:
        raise credentials_exception
    
    token_data_str = redis_client.get(f"session:{token}")
    if not token_data_str:
        raise credentials_exception

    token_data = json.loads(token_data_str)
    user_id = token_data.get("user_id")
    if not user_id:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    return user

async def login(request: Request, db: Session = Depends(SessionLocal)):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    user = db.query(User).filter(User.username == username).first()
    if not user or not user.check_password(password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_id = str(uuid.uuid4())
    access_token = token_id

    store_token(token_id=token_id, token=access_token, expires_in=EXPIRES, user_id=user.id)

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(key="ssid", value=access_token, max_age=EXPIRES, httponly=True, path="/", secure=False, samesite="lax")

    return response
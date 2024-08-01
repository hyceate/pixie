from datetime import datetime, timedelta
from aioredis import ResponseError
from fastapi import Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from ...db import redis_client, get_db
from ...models import User, Session
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

def delete_session_from_db(token_id: str, db: Session):
    session = db.query(Session).filter(Session.token == token_id).first()
    if session:
        try:
            db.delete(session)
            db.commit()
        except ResponseError as e:
            print(f"Error deleting from postgres database: {e}")

def delete_token(token_id: str):
    key = f"session:{token_id}"
    try:
        redis_client.delete(key)
    except ResponseError as e:
        print(f"Redis ResponseError while deleting token: {e}")

def get_token_data(token_id: str):
    key = f"session:{token_id}"

    session_data = redis_client.hgetall(key)

    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_data

async def login(request: Request, db: Session = Depends(get_db)):
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

    expires_in = timedelta(seconds=EXPIRES)
    expires_at = datetime.now() + expires_in

    session_token = Session(token_id=token_id, user_id=user.id, expires_at=expires_at)
    db.add(session_token)
    db.commit()

    redis_client.hset(f"session:{access_token}", mapping={
        "user_id": str(user.id),
        "expires_at": expires_at.isoformat()
    })
    redis_client.expire(f"session:{access_token}", EXPIRES)

    # Create response
    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(key="ssid", value=access_token, max_age=EXPIRES, httponly=True, path="/", secure=False, samesite="lax")

    return response
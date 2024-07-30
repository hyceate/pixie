from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from tortoise.exceptions import ValidationError
from pydantic import BaseModel
from dotenv import load_dotenv
from ..models import User
from ..db import redis_client
import os
import uuid
import json

load_dotenv()

router = APIRouter(prefix="/auth")

secret = os.getenv('SECRET_KEY', 'your-secret-key')
SESSION_COOKIE_NAME = 'ssid'
SESSION_EXPIRATION = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class RegisterRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

async def create_user(username: str, display_name: str, password: str):
    if await User.filter(username=username).exists():
        raise ValidationError("Username already taken")
    user = User(username=username, display_name=display_name)
    user.set_password(password)
    await user.save()
    
    return user

def store_token(token_id: str, token: str, expires_in: int, user_id: uuid.UUID):
    user_id_str = str(user_id)
    token_data = {
        "token": token,
        "user_id": user_id_str
    }
    token_data_str = json.dumps(token_data)
    redis_client.setex(f"session:{token_id}", expires_in, token_data_str)

def get_token(token_id: str) -> str:
    return redis_client.get(f"session:{token_id}")

def delete_token(token_id: str):
    redis_client.delete(f"session:{token_id}")

def get_token_data(token_id: str):
    token_data_str = redis_client.get(f"session:{token_id}")
    if token_data_str:
        print(f"Token Data Retrieved: {token_data_str}")
        return json.loads(token_data_str)
    print("No Token Data Found")
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = get_token_data(token_id=token)
    if not token_data or token_data["token"] != token:
        raise credentials_exception
    
    user_id = uuid.UUID(token_data["user_id"])
    user = await User.filter(id=user_id).first()
    if user is None:
        raise credentials_exception
    
    return user

@router.post("/register")
async def register(request: Request):
    data = await request.json()
    username = data.get('username')
    display_name = data.get('display_name')
    password = data.get('password')

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    if await User.filter(username=username).first() is not None:
        raise HTTPException(status_code=400, detail="User already exists")

    try:
        user = await create_user(username, display_name, password)
        return {"message": "User created successfully", "user_id": user.id}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    user = await User.filter(username=username).first()
    if not user or not user.check_password(password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_id = str(uuid.uuid4())
    access_token = token_id

    store_token(token_id=token_id, token=access_token, expires_in=SESSION_EXPIRATION * 60, user_id=user.id)

    response = JSONResponse(content={"message": "Login successful"})
    if request.cookies.get("ssid"):
        response.delete_cookie("ssid")
    response.set_cookie(key="ssid", value=access_token, max_age=SESSION_EXPIRATION * 60, httponly=True, path="/", secure=False, samesite="lax")
    return response

@router.post("/logout")
async def logout(request: Request):
    token = request.cookies.get("ssid")
    print("removing cookie", token)
    if not token:
        raise HTTPException(status_code=400, detail="Token missing")
    
    delete_token(token_id=token)

    response = JSONResponse(content={"message": "Logout successful"})
    response.delete_cookie("ssid")
    return {"message": "Logout successful"}

@router.get("/protected")
async def read_protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you have access to this protected route."}

@router.get("/get-token")
def getToken(request:Request):
    token = request.cookies.get("ssid")
    tokenData = get_token_data(token_id=token)
    
    return {"message": f"{token}, {tokenData}"}
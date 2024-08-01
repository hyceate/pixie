from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from uuid import UUID
from .controllers.auth_controllers import *
from dotenv import load_dotenv
from ..db import get_db

load_dotenv()

router = APIRouter(prefix="/auth")

class UserBase(BaseModel):
    username: str
    display_name: str

class UserCreate(UserBase):
    password:str

class UserResponseModel(BaseModel):
    id: UUID
    username: str
    display_name: str

    class Config:
        from_attributes = True

@router.post("/register", response_model=UserResponseModel)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = await create_user(user.username, user.display_name, user.password, db)
    return new_user
    
@router.post("/login")
async def login_route(request: Request, db: Session = Depends(get_db)):
    response = await login(request, db)
    return response

@router.post("/logout")
async def logout(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("ssid")
    if not token:
        raise HTTPException(status_code=400, detail="Token missing")

    delete_session_from_db(token_id=token, db=db)
    delete_token(token_id=token)

    response = JSONResponse(content={"message": "Logout successful"})
    response.delete_cookie("ssid")
    return response

@router.get("/protected")
async def read_protected_route(request: Request):
    current_user = request.state.user
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return {"message": f"Hello {current_user.username}, you have access to this protected route."}

@router.get("/get-token")
def get_token(request: Request):
    session_id = request.cookies.get("ssid")
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID missing in cookies")
    
    try:
        session_data = get_token_data(session_id)
    except HTTPException as e:
        raise e
    except redis_client.exceptions.RedisError as e:
        raise HTTPException(status_code=500, detail="Redis error occurred")

    session_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in session_data.items()}
    return {"session_data": session_data}
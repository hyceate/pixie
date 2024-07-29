from fastapi import APIRouter, Request, HTTPException
from tortoise.exceptions import ValidationError
from ..sql_models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/auth")

class RegisterRequest(BaseModel):
    username: str
    password: str
    
async def create_user(username: str, password: str):
    if await User.filter(username=username).exists():
        raise ValidationError("Username already taken")
    user = User(username=username)
    user.set_password(password)
    await user.save()
    
    return user

@router.post("/register")
async def register(request: Request):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    if await User.filter(username=username).first() is not None:
        raise HTTPException(status_code=400, detail="User already exists")

    try:
        user = await create_user(username, password)
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

    # Here you would usually return a token
    return {"message": "Login successful"}

@router.post("/logout")
async def logout():
    # * to do
    return {"message": "Logout successful"}
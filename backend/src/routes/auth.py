from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from tortoise.exceptions import ValidationError
from .controllers.auth_controllers import *
from dotenv import load_dotenv
from ..models import User

load_dotenv()

router = APIRouter(prefix="/auth")

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
async def login_route(request: Request):
    response = await login(request)
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
async def read_protected_route(request: Request):
    current_user = await get_current_user(request)
    return {"message": f"Hello {current_user.username}, you have access to this protected route."}

@router.get("/get-token")
def getToken(request:Request):
    token = request.cookies.get("ssid")
    tokenData = get_token_data(token_id=token)
    
    return {"message": f"{token}, {tokenData}"}
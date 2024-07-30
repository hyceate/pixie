from fastapi import APIRouter, HTTPException
from ..db import *

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@router.get("/test-redis")
async def test_redis():
    try:
        redis_client.set("test_key", "test_value")

        value = redis_client.get("test_key")
        
        if value is None:
            raise HTTPException(status_code=500, detail="Failed to retrieve value from Redis")
        
        # Using a f-string for embed
        return {"status": "success", "message": f"Connected to Redis. Retrieved value: {value.decode('utf-8')}"}
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Redis connection error: {str(e)}")
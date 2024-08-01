from dotenv import load_dotenv
import redis
import os
from .config import SessionLocal

load_dotenv()
redis_host = os.getenv('REDIS_HOST','localhost')
redis_client = redis.Redis(host=redis_host, port=6379, db=0)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
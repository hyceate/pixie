from tortoise import Tortoise
from .config import TORTOISE_ORM
from dotenv import load_dotenv
import redis
import os

load_dotenv()
redis_host = os.getenv('REDIS_HOST','localhost')
redis_client = redis.Redis(host=redis_host, port=6379, db=0)

async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

async def close_db_connections():
    await Tortoise.close_connections()

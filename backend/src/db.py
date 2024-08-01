from dotenv import load_dotenv
import redis
import os

load_dotenv()
redis_host = os.getenv('REDIS_HOST','localhost')
redis_client = redis.Redis(host=redis_host, port=6379, db=0)
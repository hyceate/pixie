from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from ..db import redis_client

class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        session_key = request.cookies.get("ssid")
        if session_key:
            token_data = redis_client.hgetall(f"session:{session_key}")
            if token_data:
                token_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in token_data.items()}
                request.state.user = token_data.get("user_id")
                print(request.state.user)
            else:
                request.state.user = None
        else:
            request.state.user = None

        return response

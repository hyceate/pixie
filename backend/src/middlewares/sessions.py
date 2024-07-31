from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from ..db import redis_client
import json


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        session_key = request.cookies.get("ssid")
        if session_key:
            token_data = redis_client.get(f"session:{session_key}")
            if token_data:
                request.state.user = json.loads(token_data).get("user_id")
            else:
                request.state.user = None
        else:
            request.state.user = None

        return response

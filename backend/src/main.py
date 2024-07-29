from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, base
from ariadne.asgi import GraphQL
from dotenv import load_dotenv
from .db import init_db, close_db_connections
from .gql.schema import schema
import os

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
schema = schema

# Create FastAPI app
async def lifespan_handler(app: FastAPI):
    await init_db()
    try:
        yield
    finally:
        await close_db_connections()

app = FastAPI(lifespan=lifespan_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],   
    allow_headers=["Authorization", "Content-Type"],
)
        
# GraphQL route
graphql_app = GraphQL(schema, debug=True)
app.mount("/graphql", graphql_app)

# routers
app.include_router(base.router)
app.include_router(auth.router)

if __name__ == '__main__':
    import uvicorn
    port = int(os.getenv('PORT', 3000))
    uvicorn.run(app, host='0.0.0.0', port=port)

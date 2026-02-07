# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from sqlmodel import create_engine, SQLModel
# import json

# from core.config import settings
# from api.endpoints import tasks, auth, chat
# from ai_agent.main import ai_router

# app = FastAPI(
#     title="Todo App",
#     openapi_url=f"{settings.API_V1_STR}/openapi.json"
# )

# # CORS - Parse origins from JSON array
# origins = []
# if settings.BACKEND_CORS_ORIGINS:
#     try:
#         # Try to parse as JSON array first (for Railway/Vercel env vars)
#         origins = json.loads(settings.BACKEND_CORS_ORIGINS)
#         print(f"✅ CORS origins parsed from JSON: {origins}")
#     except (json.JSONDecodeError, TypeError):
#         # Fallback: split by comma for string format (for local .env)
#         origins = [str(origin).strip() for origin in settings.BACKEND_CORS_ORIGINS.split(",")]
#         print(f"✅ CORS origins parsed from string: {origins}")

# print(f"CORS origins configured: {origins}")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
#     allow_headers=["*"],
# )

# engine = create_engine(settings.DATABASE_URL, echo=True)

# from sqlalchemy.exc import OperationalError

# @app.on_event("startup")
# def on_startup():
#     try:
#         SQLModel.metadata.create_all(engine)
#     except OperationalError as e:
#         print(f"ERROR: Could not connect to database on startup. Please ensure the database is running and accessible. Error: {e}")

# app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
# app.include_router(tasks.router, prefix=f"{settings.API_V1_STR}", tags=["tasks"])
# app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
# app.include_router(ai_router, prefix=f"{settings.API_V1_STR}/ai", tags=["ai"])





from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import create_engine, SQLModel
import json
import os

from core.config import settings
from api.endpoints import tasks, auth, chat
from ai_agent.main import ai_router

app = FastAPI(
    title="Todo App",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS - Parse origins from JSON array
origins = []
if settings.BACKEND_CORS_ORIGINS:
    try:
        # Try to parse as JSON array first (for Railway/Vercel env vars)
        origins = json.loads(settings.BACKEND_CORS_ORIGINS)
        print(f"✅ CORS origins parsed from JSON: {origins}")
    except (json.JSONDecodeError, TypeError):
        # Fallback: split by comma for string format (for local .env)
        origins = [str(origin).strip() for origin in settings.BACKEND_CORS_ORIGINS.split(",")]
        print(f"✅ CORS origins parsed from string: {origins}")

# Add Hugging Face deployment CORS support
frontend_url = os.getenv("FRONTEND_URL", "")
if frontend_url and frontend_url not in origins:
    origins.append(frontend_url)
    print(f"✅ Added FRONTEND_URL to CORS: {frontend_url}")

print(f"CORS origins configured: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

engine = create_engine(settings.DATABASE_URL, echo=True)

from sqlalchemy.exc import OperationalError

@app.on_event("startup")
def on_startup():
    try:
        SQLModel.metadata.create_all(engine)
    except OperationalError as e:
        print(f"ERROR: Could not connect to database on startup. Please ensure the database is running and accessible. Error: {e}")

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(tasks.router, prefix=f"{settings.API_V1_STR}", tags=["tasks"])
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
app.include_router(ai_router, prefix=f"{settings.API_V1_STR}/ai", tags=["ai"])
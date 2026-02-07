# This file is intentionally left blank.
# Routers are aggregated in main.py.
# If you wish to aggregate routers here, you could do something like:
#
# from fastapi import APIRouter
# from .endpoints import auth, tasks, chat
#
# api_router = APIRouter()
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(tasks.router, tags=["tasks"])
# api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
#
# Then, in main.py:

# app.include_router(api_router, prefix=settings.API_V1_STR)


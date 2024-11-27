from io import BytesIO
from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_setup import get_session


from utils.chat import chat_func

chat_router = APIRouter()

@chat_router.websocket('/ws')
async def chat_path(ws: WebSocket):
    return await chat_func(ws)
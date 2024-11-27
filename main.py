from sys import prefix

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import config
from routes.document import document_router
from routes.chat import chat_router
from db.db_setup import init_db
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan, debug=config.DEBUG, title='baza')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(document_router, prefix='/doc', tags=['registration'])
app.include_router(chat_router, prefix='/chat', tags=['chat'])


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, timeout_keep_alive=60, port=8001)

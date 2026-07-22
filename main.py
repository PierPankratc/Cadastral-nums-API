from fastapi import FastAPI
import uvicorn
import asyncio
from multiprocessing import Process
from app.routers import router
from app.init_db import init_db

app = FastAPI()
app.include_router(router)


async def init_app():
    await init_db()


if __name__ == "__main__":
    asyncio.run(init_app())

    

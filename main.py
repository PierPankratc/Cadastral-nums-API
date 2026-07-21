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


def start_fake_service():
    uvicorn.run("fake_servis:fake_servis", host="127.0.0.1", port=8001, log_level="info")


if __name__ == "__main__":
    asyncio.run(init_app())

    fake_process = Process(target=start_fake_service, daemon=True)
    fake_process.start()

    try:
        uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')
    finally:
        fake_process.terminate()
        fake_process.join(timeout=3)
    

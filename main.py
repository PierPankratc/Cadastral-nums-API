from fastapi import FastAPI
import uvicorn
import asyncio
from app.routers import router
from app.init_db import init_db
from fake_servis import fake_servis

app = FastAPI()
app.include_router(router)
app.mount('/fake', fake_servis)

async def init_app():
    await init_db()


if __name__ == "__main__":
    asyncio.run(init_app())
    uvicorn.run(app, host='127.0.0.1', port=8000)
    

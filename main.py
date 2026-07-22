from fastapi import FastAPI
import uvicorn
from app.routers import router
from app.init_db import init_db

app = FastAPI()
app.include_router(router)

async def init_app():
    await init_db()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)

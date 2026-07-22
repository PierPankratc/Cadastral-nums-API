import asyncio
import random
from fastapi import FastAPI

fake_service = FastAPI()


@fake_service.get("/result")
async def response():
    random_time = random.uniform(1, 60)
    await asyncio.sleep(random_time)
    result = random.choice([True, False])
    return {"result": result}

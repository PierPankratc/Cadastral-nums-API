import asyncio
import random
from fastapi import FastAPI

fake_servis = FastAPI()

@fake_servis.get('/result')
async def response():
    random_time = random.uniform(0.1, 0.5)
    await asyncio.sleep(random_time)
    result = random.choice([True, False])
    return {'result': result}

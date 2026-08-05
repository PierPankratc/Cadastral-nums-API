import subprocess

import httpx
import pytest
import uvicorn

from app.routers import start, ping, history, query

@pytest.fixture
def get_url():
    return 'http://127.0.0.1:8000'

@pytest.fixture
async def run_server():
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
    async with httpx.AsyncClient() as client:
        resp = await client.get(url='http://127.0.0.1:8000')
        if resp.status_code == 200:
            yield





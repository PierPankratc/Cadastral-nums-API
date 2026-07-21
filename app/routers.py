from fastapi import APIRouter
from app.schemas import AddCadastralNumber
from app.init_db import connect_db
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

FAKE_SERVIS_URL = os.getenv('FAKE_SERVIS_URL', 'http://localhost:8001')

router = APIRouter()


@router.post('/query')
async def query(cadastr_number: AddCadastralNumber):
    cursor = await connect_db()
    try:
        async with httpx.AsyncClient() as client:
            servis_resp = await client.get(url=f"{FAKE_SERVIS_URL}/result")
            servis_result = servis_resp.json().get('result')

        await cursor.execute(
            """
            INSERT INTO cadastral_info(cadastral_number, latitude, longitude, server_response)
            VALUES($1, $2, $3, $4);
            """,
            cadastr_number.cadastral_number,
            str(cadastr_number.latitude),
            str(cadastr_number.longitude),
            servis_result,
        )
        return {'status': 'success', 'result': servis_result}
    finally:
        await cursor.close()


@router.get('/ping')
async def ping():
    async with httpx.AsyncClient() as client:
        resp = await client.get(url=f"{FAKE_SERVIS_URL}/result")
        result = resp.json().get('result')
        return {'status': 'success', 'result': result}


@router.get('/history')
async def history():
    cursor = await connect_db()
    try:
        rows = await cursor.fetch(
            """
            SELECT * FROM cadastral_info
            """
        )
        result = [dict(row) for row in rows]
        return {'status': 'success', 'cadastr_list': result}
    finally:
        await cursor.close()
    

    



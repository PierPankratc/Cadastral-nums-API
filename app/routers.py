from fastapi import APIRouter, HTTPException
from app.schemas import AddCadastralNumber
from app.init_db import connect_db
from fastapi.testclient import TestClient
from dotenv import load_dotenv
import httpx
import asyncpg

load_dotenv()

from fake_servis import fake_servis
client = TestClient(fake_servis)

router = APIRouter()


@router.post('/query')
async def query(cadastr_number: AddCadastralNumber):
    cursor = None
    try:
        cursor = await connect_db()
        servis_resp = client.get('/result')
        if servis_resp.status_code != 200:
            raise HTTPException(status_code=502, detail='Fake service error')
        servis_result = servis_resp.json().get('result')
        if servis_result is None:
            raise HTTPException(status_code=502, detail='Invalid fake service response')

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
    except httpx.ReadTimeout:
        raise HTTPException(status_code=504, detail='Fake service timeout')
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f'Fake service error: {exc}')
    except asyncpg.PostgresError as exc:
        raise HTTPException(status_code=500, detail=f'Database error: {exc}')
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f'Unknown server error: {exc}')
    finally:
        if cursor is not None:
            await cursor.close()


@router.get('/ping')
async def ping():
    resp = client.get('/result')
    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail='Fake service error')
    result = resp.json().get('result')
    if result is None:
        raise HTTPException(status_code=502, detail='Invalid fake service response')
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
    

    



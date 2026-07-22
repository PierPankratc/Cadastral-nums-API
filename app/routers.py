from fastapi import APIRouter, HTTPException
from app.schemas import AddCadastralNumber
from app.init_db import connect_db
from dotenv import load_dotenv
import httpx
import asyncpg
import os


load_dotenv()

FAKE_SERVICE_BASE_URL = os.getenv('FAKE_SERVICE_URL', 'http://127.0.0.1:8001')


router = APIRouter()


@router.post('/query')
async def query(cadastr_number: AddCadastralNumber):

    try:
        cursor = await connect_db()
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.get(f"{FAKE_SERVICE_BASE_URL}/result")
            resp.raise_for_status()
            servis_result = resp.json().get('result')

        if servis_result is None:
            raise HTTPException(status_code=502, detail='Invalid fake service response')

        await cursor.execute(
            """
            INSERT INTO cadastral_info(cadastral_number, latitude, longitude, server_response)
            VALUES($1, $2, $3, $4);
            """,
            str(cadastr_number.cadastral_number),
            str(cadastr_number.latitude),
            str(cadastr_number.longitude),
            servis_result,
        )
        return {'status': 'success', 
                'result': servis_result}
    except httpx.ReadTimeout:
        raise HTTPException(status_code=504, detail='Fake service timeout')
    
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f'Fake service error: {exc.response.status_code}')
    
    except httpx.RequestError as exc:
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
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.get(f"{FAKE_SERVICE_BASE_URL}/result")
            resp.raise_for_status()
            result = resp.json().get('result')

        if result is None:
            raise HTTPException(status_code=502, detail='Invalid fake service response')
        return {'status': 'success', 'result': result}
    except httpx.ReadTimeout:
        raise HTTPException(status_code=504, detail='Fake service timeout')
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f'Fake service error: {exc.response.status_code}')
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f'Fake service error: {exc}')



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
    

    




import asyncio
import os
from pprint import pprint
import  asyncpg
from dotenv import load_dotenv

load_dotenv()
DSN = os.getenv('DSN', 'postgres://user:pass@localhost:5432/test_case')

async def connect_db():
    cursor = await asyncpg.connect(DSN)
    return cursor

async def init_db():
    cursor = await connect_db()
    try:  
        await cursor.execute("""
        CREATE DATABASE IF NOT EXISTS test_case;
    """)
        await cursor.execute("""
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    """)
        await cursor.execute("""
        CREATE TABLE IF NOT EXISTS cadastral_info(
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        cadastral_number Varchar NOT NULL UNIQUE,
        latitude VARCHAR(30) NOT NULL,
        longitude VARCHAR(30) NOT NULL,
        created_at timestamp  DEFAULT current_timestamp  NOT NULL,
        server_response BOOLEAN NOT NULL
    );""")
    except Exception as e:
        return e
    finally:
        await cursor.close()


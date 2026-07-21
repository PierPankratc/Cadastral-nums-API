import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()
DSN = os.getenv('DSN', 'postgres://user:pass@localhost:5432/test_case')

async def connect_db():
    return await asyncpg.connect(DSN)

async def init_db():
    connection = None
    try:
        connection = await connect_db()
        await connection.execute(
            """
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
            """
        )
        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS cadastral_info(
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                cadastral_number VARCHAR NOT NULL UNIQUE,
                latitude VARCHAR(30) NOT NULL,
                longitude VARCHAR(30) NOT NULL,
                created_at TIMESTAMP DEFAULT current_timestamp NOT NULL,
                server_response BOOLEAN NOT NULL
            );
            """
        )
    finally:
        if connection is not None:
            await connection.close()


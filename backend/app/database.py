"""
database.py
"""

# Imports
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os
from typing import AsyncGenerator

DATABASE_URL = os.getenv("DATABASE_URL")

async_engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

# FASTAPI dependency function
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

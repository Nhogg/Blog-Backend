"""
main.py
    Define FastAPI endpoints and async logic.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, AsyncGenerator
from contextlib import asynccontextmanager

from . import schemas, models, crud, database


# Lifespan context manager for startup logic
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    async with database.async_engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get async DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with database.async_session() as session:
        yield session


# Routes
@app.get("/posts/", response_model=List[schemas.PostOut])
async def get_posts(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_posts(db, skip=skip, limit=limit)


@app.get("/posts/{slug}", response_model=schemas.PostOut)
async def get_post(slug: str, db: AsyncSession = Depends(get_db)):
    post = await crud.get_post_by_slug(db, slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.post("/posts/", response_model=schemas.PostOut)
async def create_post(post: schemas.PostCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_post(db, post)


@app.put("/posts/{slug}", response_model=schemas.PostOut)
async def update_post(slug: str, post: schemas.PostCreate, db: AsyncSession = Depends(get_db)):
    updated_post = await crud.update_post(db, slug, post)
    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post


@app.delete("/posts/{slug}")
async def delete_post(slug: str, db: AsyncSession = Depends(get_db)):
    await crud.delete_post(db, slug)
    return {"ok": True}

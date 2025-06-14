"""
main.py
    Provides a FastAPI entry point and interface, as well as CORS middleware.
"""
# Imports
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import schemas, models, crud, database

# Declare app interface
app = FastAPI()

# Enable CORS to allow frontend dev server to function
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

# Define endpoints
@app.get("/posts/", response_model=list[schemas.PostOut])
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_posts(db, skip=skip, limit=limit)

@app.get("/posts/{slug}", response_model=schemas.PostOut)
def get_post(slug: str, db: Session = Depends(database.get_db)):
    post = crud.get_post_by_slug(db, slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post("/posts/", response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db)):
    return crud.create_post(db, post)

@app.put("/posts/{slug}", response_model=schemas.PostOut)
def update_post(slug: str, post: schemas.PostCreate, db: Session = Depends(database.get_db)):
    return crud.update_post(db, slug, post)

@app.delete("/posts/{slug}")
def delete_post(slug: str, db: Session = Depends(database.get_db)):
    crud.delete_post(db, slug)
    return {"ok": True}

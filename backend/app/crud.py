"""
crud.py
    Define create, read, update, delete model for DB interaction and posting.
"""

from sqlalchemy.orm import Session
from . import models, schemas, markdown_utils

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()

def get_post_by_slug(db: Session, slug: str):
    return db.query(models.Post).filter(models.Post.slug == slug).first()

def create_post(db: Session, post: schemas.PostCreate):
    html = markdown_utils.convert_markdown_to_html(post.markdown)
    db_post = models.Post(**post.model_dump(), html=html)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, slug: str, post: schemas.PostCreate):
    db_post = get_post_by_slug(db, slug)
    if db_post:
        db_post.title = post.title
        db_post.markdown = post.markdown
        db_post.html = markdown_utils.convert_markdown_to_html(post.markdown)
        db.commit()
        db.refresh(db_post)
    return db_post

def delete_post(db: Session, slug: str):
    db_post = get_post_by_slug(db, slug)
    if db_post:
        db.delete(db_post)
        db.commit()
"""
crud.py
    Define create, read, update, delete model for DB interaction and posting.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas, markdown_utils
import re
from .schemas import PostCreate
from datetime import datetime

async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Post).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_post_by_slug(db: AsyncSession, slug: str):
    result = await db.execute(
        select(models.Post).filter(models.Post.slug == slug)
    )
    return result.scalars().first()

async def create_post(db: AsyncSession, post: PostCreate):
    slug = post.slug or slugify(post.title)
    markdown = post.markdown or post.content  # or convert_to_markdown(post.content)
    html = markdown_utils.convert_markdown_to_html(markdown)

    db_post = models.Post(
        title=post.title,
        content=post.content,
        slug=slug,
        markdown=markdown,
        html=html,
        created_at=datetime.now()
    )
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

async def update_post(db: AsyncSession, slug: str, post: schemas.PostCreate):
    db_post = await get_post_by_slug(db, slug)
    if db_post:
        db_post.title = post.title
        db_post.markdown = post.markdown
        db_post.html = markdown_utils.convert_markdown_to_html(post.markdown)
        await db.commit()
        await db.refresh(db_post)
    return db_post

async def delete_post(db: AsyncSession, slug: str):
    db_post = await get_post_by_slug(db, slug)
    if db_post:
        await db.delete(db_post)
        await db.commit()

# Util
def slugify(title: str) -> str:
    """
    Auto-generate slug from title.
    :param title: post title
    :return: slugged title
    """
    return re.sub(r'\W+', '-', title.lower()).strip('-')
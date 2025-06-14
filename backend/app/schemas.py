'''
schemas.py
    Provide Pydantic schemas
'''

# Imports
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    slug: str
    markdown: str

class PostCreate(PostBase):
    title: str
    content: str
    slug: Optional[str] = None
    markdown: Optional[str] = None

class PostOut(PostBase):
    html: str
    created_at: datetime

    class Config:
        orm_mode = True
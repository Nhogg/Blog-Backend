'''
schemas.py
    Provide Pydantic schemas
'''

# Imports
from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    slug: str
    markdown: str

class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    html: str
    created_at: datetime

    class Config:
        orm_mode = True
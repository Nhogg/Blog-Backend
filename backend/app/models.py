"""
models.py
    Define SQLAlchemy ORM.
"""

# Imports
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    slug = Column(String, index=True, unique=True)
    markdown = Column(String)
    html = Column(Text)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.time(datetime.now()))



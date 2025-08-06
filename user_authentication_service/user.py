#!/usr/bin/env python3
"""
user file
"""


from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

# Create a base class
Base = declarative_base()

class User(Base):
    """ SQLAlchemy model for a user """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(128), nullable=False, unique=True)
    hashed_password = Column(String(128), nullable=False)
    session_id = Column(String(128), nullable=True)
    reset_token = Column(String(128), nullable=True)

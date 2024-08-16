#!/usr/bin/env python3
"""Module for User model class"""
from sqlalchemy import Column, Integer, String  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from typing import Any


Base: Any = declarative_base()


class User(Base):
    """User class: model for the users table in the database"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

#!/usr/bin/env python3
"""
Module for the DB management class
"""
from user import Base
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from user import User
from sqlalchemy.exc import InvalidRequestError, NoResultFound


class DB:
    """
    DB class to manage the database connection
    """

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user based on the given user_id and keyword arguments
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            # skip the id and hashed_password attributes
            if key in ["id"]:
                continue
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")
        self._session.commit()

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database based on the given keyword arguments
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
        except NoResultFound:
            raise NoResultFound("No matching results found")
        except InvalidRequestError:
            raise InvalidRequestError("Incorrect query arguments")

        if user is None:
            raise NoResultFound("No matching results found")
        return user

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database
        """
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            self.__session.rollback()
            return
        return user

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

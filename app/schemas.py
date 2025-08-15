from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class Postbase(BaseModel):
    title: str
    caption: str
    content: str
    published : bool = True

    class Config:      #  This class is used because this tells Pydantic to treat SQLAlchemy ORM objects like dictionaries, so they can be serialized properly in the response model.
                        #Pydantic expects a regular Python dict and SQLAlchemy models are not dicts.
        from_attributes = True

class postcreate(Postbase):
    pass


class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:      #  This class is used because this tells Pydantic to treat SQLAlchemy ORM objects like dictionaries, so they can be serialized properly in the response model.
                        #Pydantic expects a regular Python dict and SQLAlchemy models are not dicts.
        from_attributes = True


class Post(Postbase):
    id : int
    created_at : datetime
    owner_id: int
    owner: UserOut

    class Config:      #  This class is used because this tells Pydantic to treat SQLAlchemy ORM objects like dictionaries, so they can be serialized properly in the response model.
                        #Pydantic expects a regular Python dict and SQLAlchemy models are not dicts.
        from_attributes = True


class postOut(BaseModel):
    Post: Post
    votes: int
    class Config:      #  This class is used because this tells Pydantic to treat SQLAlchemy ORM objects like dictionaries, so they can be serialized properly in the response model.
                        #Pydantic expects a regular Python dict and SQLAlchemy models are not dicts.
        from_attributes = True


class UserCreate(BaseModel):
    email : EmailStr
    password : str
    # id : int
    # created_at : datetime
    class Config:      #  This class is used because this tells Pydantic to treat SQLAlchemy ORM objects like dictionaries, so they can be serialized properly in the response model.
                        #Pydantic expects a regular Python dict and SQLAlchemy models are not dicts.
        from_attributes = True




class userLogin(BaseModel):
    email : EmailStr
    password : str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None


class Votes(BaseModel):
    post_id: int
    dir: conint(ge=0,le=1)

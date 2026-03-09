# We are creating a social media-like app API
from typing import Optional
from pydantic import BaseModel

""" We would need
-> surname
-> firstname
-> other_names
-> username
-> email
-> phone contact (primary key)
-> password
-> post
-> likes
-> dislikes
"""

class User_Info(BaseModel):
    surname: str
    firstname:str
    other_name:str = ""
    username:str
    email:str
    phone_contact: str
    id:int = ''
    signed_up_at:Optional[str] = ''

class Personal_Info(BaseModel):
    surname: str
    firstname:str
    other_names:str
    id:int = ''

class Set_Personal_Info(BaseModel):
    surname: str
    firstname:str
    other_names:str

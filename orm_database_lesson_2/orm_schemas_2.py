import datetime

from pydantic import BaseModel, EmailStr, conint
from typing import Optional


# Schema for storing user's registration data to database
class UserRegData(BaseModel):

    id : Optional[int] = None
    username : str
    email : EmailStr
    password :str
    created_at : datetime.datetime = datetime.datetime.now()
    confirmed_password : str = ""



    class Config:
        #orm_mode = True
        from_attributes = True

# Schema for storing user's personal data to database
class UserPersonalData(BaseModel):
    id: Optional[int] = None
    username: str
    email: EmailStr
    created_at: datetime.datetime = datetime.datetime.now()
    surname: str
    firstname: str
    other_names: str = ""
    is_adult: bool
    confirmed_password: str


    class Config:
        #orm_mode = True
        from_attributes = True

# Schema for storing user's post data to database
class UserPosts(BaseModel):

    id : Optional[int] = None
    postUserId: int
    username : str
    email : EmailStr
    postTitle : str
    postContent : str
    createdAt: datetime.datetime = datetime.datetime.now()
    class Config:
        #orm_mode = True
        from_attributes = True

# Schema for displaying user's updated post data from and collecting user's updated post data to, database
class UpdatePost(BaseModel):
    username: str
    email: EmailStr
    postContent: str
    lastUpdatedAt: datetime.datetime = datetime.datetime.now()

    class Config:
        #orm_mode = True
        from_attributes = True

# Schema for displaying user's registration data from database
class UserAccount(BaseModel):
    fullname: str
    username: str
    is_adult: bool = True
    email: EmailStr

    class Config:
        # orm_mode = True
        from_attributes = True

# Schema for displaying user's post data from and collecting user's post data to, database
class CreatePost(BaseModel):

    username: str
    email: EmailStr
    postTitle: str
    postContent: str
    postUserId: int=0
    createdAt: datetime.datetime = datetime.datetime.now()

    class Config:
        #orm_mode = True
        from_attributes = True

class LoginResponse(BaseModel):
    email: EmailStr
    status: str="Login Successful"

class Token(BaseModel):
    access_token: str
    token_type: str ="bearer"

class TokenResponse(Token):
    id_: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, gt=0)
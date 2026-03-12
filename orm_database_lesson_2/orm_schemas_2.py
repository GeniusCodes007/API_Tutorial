import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional

# For Our Tables

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
    up_votes : int = 0
    down_votes : int = 0
    createdAt: datetime.datetime = datetime.datetime.now()
    class Config:
        #orm_mode = True
        from_attributes = True

# Schema for registering the users' votes on posts
class PostVotes(BaseModel):
    post_id: int
    user_id: int
    vote_postTitle: str
    vote_Author_Email: EmailStr
    vote_Author_Username: str
    up_votes_users: list[str] = []
    down_votes_users: list[str] = []

    class Config:
        from_attributes = True



# Other Schemas

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
    #id: int
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
    token_id: Optional[str] = None

class Vote(BaseModel):
    post_title: str
    post_author_username_or_email: str
    is_up_vote: bool

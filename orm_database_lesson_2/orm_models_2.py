

from sqlalchemy import Integer, String, Column, Boolean, ForeignKey
from orm_database_2 import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP



class Personal_Data(Base):
    __tablename__ = "personal_data"

    id = Column(Integer, primary_key=True, nullable=False)
    surname = Column(String, nullable=False)
    firstname= Column(String, nullable=False)
    other_names = Column(String, nullable=False, server_default='')
    username = Column(String(length=15), nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    is_adult= Column(Boolean, nullable=False, server_default='0')
    created_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    confirmed_password = Column(String, nullable=False)

class User_Reg_Data(Base):
    __tablename__ = "user_reg_data"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(15), nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False )
    created_at= Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    confirmed_password = Column(String, nullable=False)

class User_Posts(Base):
    __tablename__ = "user_posts"

    id = Column(Integer, primary_key=True, nullable=False)
    postUserId = Column(Integer, ForeignKey("user_reg_data.id", ondelete="CASCADE"), nullable=False,  )
    username = Column(String(25), nullable=False)
    email = Column(String, nullable=False)
    postTitle = Column(String, nullable=False)
    postContent = Column(String, nullable=False, unique=True)
    createdAt= Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    lastUpdatedAt= Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "post_vote"

    vote_posts_id = Column(Integer, ForeignKey("user_posts.id", ondelete="CASCADE"),primary_key=True, nullable=False)
    vote_users_id = Column(Integer, ForeignKey("user_reg_data.id", ondelete="CASCADE"),primary_key=True, nullable=False)


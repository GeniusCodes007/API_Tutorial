# uvicorn orm_main:app --reload
# "C:\Users\GENIUS DEXTER\API_Tutorial\orm_database_lesson"
#  http://127.0.0.1:8000/openapi.json


import orm_posts, orm_users, orm_auth, orm_root, orm_production, orm_votes
from fastapi import FastAPI
import psycopg2
import orm_models
from orm_database import database_engine
from config import my_settings

# Create Database Engine
orm_models.Base.metadata.create_all(bind=database_engine)

# Setup FastAPI
app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
)


try:
    # create connection to database
    connection= psycopg2.connect(host=f"{my_settings.database_hostname}", database=f"{my_settings.database_name}", user= f"{my_settings.database_username}", password=f"{my_settings.database_password}")
    conn_cursor = connection.cursor()
    print("Connected to database")
except psycopg2.Error as e:
    print(e)


# Include routers from other files within the directory and their routers
app.include_router(orm_production.router)
app.include_router(orm_root.my_router)
app.include_router(orm_posts.router)
app.include_router(orm_users.router)
app.include_router(orm_auth.router)
app.include_router(orm_votes.router)
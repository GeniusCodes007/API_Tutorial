# uvicorn orm_database_lesson_2.orm_main_2:app --reload
# "C:\Users\GENIUS DEXTER\API_Tutorial"
#  http://127.0.0.1:8000/openapi.json

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import psycopg2
import orm_database_lesson_2.orm_users_2, orm_database_lesson_2.orm_production_2, orm_database_lesson_2.orm_votes_2, \
    orm_database_lesson_2.orm_auth_2, orm_database_lesson_2.orm_root_2, orm_database_lesson_2.orm_posts_2#, orm_database_lesson_2.orm_models_2,
#from orm_database_lesson_2.orm_database_2 import database_engine
from orm_database_lesson_2.config_2 import my_settings

# Create Database Engine
#orm_database_lesson_2.orm_models_2.Base.metadata.create_all(bind=database_engine)

# Setup FastAPI
app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
)

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


try:
    # create connection to database
    connection= psycopg2.connect(host=f"{my_settings.database_hostname}", database=f"{my_settings.database_name}", user= f"{my_settings.database_username}", password=f"{my_settings.database_password}")
    conn_cursor = connection.cursor()
    print("Connected to database")
except psycopg2.Error as e:
    print(e)


# Include routers from other files within the directory and their routers
app.include_router(orm_database_lesson_2.orm_production_2.router)
app.include_router(orm_database_lesson_2.orm_root_2.my_router)
app.include_router(orm_database_lesson_2.orm_posts_2.router)
app.include_router(orm_database_lesson_2.orm_users_2.router)
app.include_router(orm_database_lesson_2.orm_auth_2.router)
app.include_router(orm_database_lesson_2.orm_votes_2.router)
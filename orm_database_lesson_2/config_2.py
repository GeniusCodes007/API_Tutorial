
from pydantic.v1 import BaseSettings
from dotenv import load_dotenv
import os
load_dotenv("C:/Users/GENIUS DEXTER/API_Tutorial/orm_database_lesson_2/.env")
class My_Settings(BaseSettings):
    database_hostname: str = os.getenv("DATABASE_HOSTNAME")
    database_port: int = os.getenv("DATABASE_PORT")
    database_password: str= os.getenv("DATABASE_PASSWORD")
    database_name: str= os.getenv("DATABASE_NAME")
    database_username: str= os.getenv("DATABASE_USERNAME")
    secret_key: str= os.getenv("SECRET_KEY")
    algorithm: str= os.getenv("ALGORITHM")
    access_token_expire_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    class Config:
        #env_prefix = "ORM_"
        env_file = ".env"


my_settings = My_Settings()
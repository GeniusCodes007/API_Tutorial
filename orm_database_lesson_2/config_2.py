
from pydantic.v1 import BaseSettings


class My_Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        #env_prefix = "ORM_"
        env_file = "../.env"


my_settings = My_Settings()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import my_settings

Base = declarative_base()



# Format with which SqlAlchemy connects with a database
#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
#SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:GENIUSCODES07@localhost/fastapi app database'

SQLALCHEMY_DATABASE_URL = f'postgresql://{my_settings.database_username}:{my_settings.database_password}@{my_settings.database_hostname}/{my_settings.database_name}'


database_engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit= False,autoflush=False ,bind=database_engine)

# Create a Database Session
def get_database():
    db_conn = SessionLocal()
    try:
        yield db_conn
    finally:
        db_conn.close()
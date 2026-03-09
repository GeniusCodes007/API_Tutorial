from fastapi import FastAPI, HTTPException, Response, status
from database_schemas import User_Info
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()
while True:
    try:
        connection = psycopg2.connect(host='localhost', database='fastapi app database', user='postgres',
                                      password='GENIUSCODES07', cursor_factory=RealDictCursor)
        my_cursor = connection.cursor()
        print("Connected to database")
        break
    except ImportError as my_error:
        print("The Issue is ",my_error)
        time.sleep(5)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/get all info")
def get_users_info():
    my_cursor.execute("""select * from user_info order by id asc""")
    info = my_cursor.fetchall()
    return info
"""surname: str
    firstname:str
    other_names:str
    username:str
    email:str
    phone_contact: str
    id:str
    signed_up_at:str"""
@app.post("/post user info")
def post_info(user_info: User_Info, response:Response):
    data =user_info.model_dump()
    try:
        my_cursor.execute("""INSERT INTO user_info ( username, surname,firstname, email, phone_contact) VALUES ($s, $s, $s, $s, $s) RETURNING * """,
                          (data["username"], data["surname"],
                           data["firstname"], data["email"],
                           data["phone_contact"]))
        user_data = my_cursor.fetchall()
        connection.commit()
        return user_data
    except Exception as e:
        print(f"FOUND THE ERROR, IT IS {e}")

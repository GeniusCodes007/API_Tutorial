from fastapi import FastAPI, HTTPException, status
import psycopg2
from database_schemas import Personal_Info, Set_Personal_Info
from psycopg2.extras import RealDictCursor

app = FastAPI()

try:
    connection = psycopg2.connect(host="localhost", database="fastapi app database", user='postgres',
                          password="GENIUSCODES07",cursor_factory=RealDictCursor)
    conn_cursor= connection.cursor()
    print("Connected to database")
except Exception as e:
    print("The error is ", e)

@app.get("/get all info")
def get_all_info():
    conn_cursor.execute("""select * from personal_data""")
    info = conn_cursor.fetchall()
    return info

@app.post("/post info", status_code=status.HTTP_201_CREATED)
def post_info(posting_info: Personal_Info):
    conn_cursor.execute("""INSERT INTO personal_data (id, surname, firstname, other_names) VALUES (%s,%s,%s,%s)""",
                        (posting_info.id, posting_info.surname, posting_info.firstname, posting_info.other_names,),)
    return f"Post Creation Successful"

@app.get("/get one info/{id_}")
def get_one_info(id_: int):
    try:
        conn_cursor.execute("""select * from personal_data where id = %s""", (str(id_),))
        test_post = conn_cursor.fetchone()
        if not test_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Data of {id_} not in database")
        return test_post
    except Exception as err :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The error is {err}    "
                                   f"Data not found")

@app.delete("/delete info/{persona_id_}")
def delete_info(persona_id_: int):
    try:
        conn_cursor.execute("""delete from personal_data where id = %s returning * """, (str(persona_id_),))
        post = conn_cursor.fetchone()
        connection.commit()
        return {"Data deleted successfully": post}
    except Exception as err :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The error is {err}    "
                                   f"Data not found")
@app.patch("/update info/{persona_id_}", status_code=status.HTTP_200_OK)
def update_info(persona_id_: int, set_person_info: Set_Personal_Info):

    conn_cursor.execute("""update personal_data set surname= %s, firstname=%s, other_names=%s where id = %s returning * """,
                        (set_person_info.surname, set_person_info.firstname, set_person_info.other_names, persona_id_,),)
    connection.commit()

@app.get("search by first letter/{name}")
def search_by_first_letter(name: str):
    conn_cursor.execute("""select * from where surname like %s""",
                        (name,),)
    post = conn_cursor.fetchall()
    return post
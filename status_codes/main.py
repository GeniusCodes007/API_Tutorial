"""
Here, we are going to be using the Pydantic schema features to extract information from our endpoints
"""

from fastapi import FastAPI, Response
from my_pydantic_models import Student_Info

app = FastAPI()

var_dict = \
    [
    {'serial_number': 1,
         'surname': "Ugwuagu",
         'first_name': "Collins",
        'other_names': "",
         'age': 10,
         'residential_address': "Home"},
    {'serial_number': 2,
         'surname': "Ngwu",
         'first_name': "Michael",
         'other_names': "Esomchi",
         'age': 10,
         'residential_address': "Home"},
    {'serial_number': 3,
         'surname': "Agu",
         'first_name': "Franklin",
         'other_names': "Ifeanyi",
         'age': 10,
         'residential_address': "Home"},
    {'serial_number': 4,
         'surname': "Onoh",
         'first_name': "Chisom",
         'other_names': "Kingsley",
         'age': 10,
         'residential_address': "Home"},
    {'serial_number': 5,
         'surname': "Ugwu",
         'first_name': "Martin",
         'other_names': "Ebuka",
         'age': 10,
         'residential_address': "Home"},
]


# CRUD OPERATIONS
# C -> Create
# R -> Read
# U -> Update
# D -> Delete

@app.post("/posts")
def create_post(my_post: Student_Info):
    my_post.serial_number = len(var_dict) +1
    var_dict.append(my_post.model_dump())
    full_Name= f"{my_post.surname} {my_post.first_name} {my_post.other_names}"
    print(full_Name)
    return var_dict

@app.get("/posts")
def get_posts():
    return var_dict

@app.get("/post/{id_}")
def get_post(id_: int, my_response: Response):
    for x in range(len(var_dict)):
        if var_dict[x]['serial_number'] == id_:
            return var_dict[x]
    return None

@app.get("/check")
def check():
    m = ()
    for x in range(len(var_dict)):
        m += (x+1,)
    for x in m:
        if var_dict[x-1]['id'] in m:
            pass
        else:
            print(f"{x} Not Here")
    return m

@app.delete("/post/{id_}")
def delete(id_: int):
    print(f"check() is {check()}")
    for x in check():
        print(f"for {x}: {var_dict[x - 1]}")
        print(f"then {var_dict[x-1]['id']}")
        if var_dict[x-1]['id'] == id_:
            wanted = var_dict[id_-1]
            print(wanted)
            var_dict.remove(wanted)
            return f"{wanted}"
    return "Not Found"
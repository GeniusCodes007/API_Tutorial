"""
Here, we are going to be using the Pydantic schema features to extract information from our endpoints
"""

from fastapi import FastAPI
from .my_pydantic_models import Student_Info

app = FastAPI()

var_dict = \
    [
    {'message 1': "Post 1 Retrieved",
     'status': "Successful",
     'id': 1},
    {'message 2': "Post 2 Retrieved",
         'status': "Successful",
     'id': 2},
    {'message 3': "Post 3 Retrieved",
         'status': "Successful",
     'id': 3},
    {'message 4': "Post 4 Retrieved",
         'status': "Successful",
     'id': 4},
    {'message 5': "Post 5 Retrieved",
         'status': "Successful",
     'id': 5},
]


# CRUD OPERATIONS
# C -> Create
# R -> Read
# U -> Update
# D -> Delete

@app.post("/post")
def create_post(my_post: Student_Info):
    my_post.id = len(var_dict) +1
    var_dict.append(my_post.model_dump())
    full_Name= f"{my_post.surname} {my_post.first_name} {my_post.other_names}"
    return full_Name, var_dict

@app.get("/posts")
def get_posts():
    return var_dict

@app.get("/post/{id_}")
def get_post(id_: int):
    for x in range(len(var_dict)):
        if var_dict[x]['id'] == id_:
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
            #print(var_dict[x-1]['id'])
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
            #print("done here")
            return f"{wanted}"
    return "Not Found"
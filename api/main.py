from fastapi import FastAPI

app = FastAPI()

var_dict = \
    {
    1: {'message': "Post 1 Retrieved",
     'status': "Successful"},
    2: {'message': "Post 2 Retrieved",
         'status': "Successful"},
    3: {'message': "Post 3 Retrieved",
         'status': "Successful"},
    4: {'message': "Post 4 Retrieved",
         'status': "Successful"},
    5: {'message': "Post 5 Retrieved",
         'status': "Successful"},
}

@app.get("/")
def home_page():
    return "First Test"

@app.get("/posts1")
def get_posts_1():
    return "Our First Posts Retrieval", var_dict

@app.get("/post1/{num}")
def get_one_post_1(num: int):
    return "Our First One Post Retrieval", var_dict[num]

#First we convert the parameter to a dictionary using the Body class from fastapi
from fastapi import Body
@app.post("/post1")
def create_post(my_post: dict=Body(...)):
    return "First Create Post", my_post
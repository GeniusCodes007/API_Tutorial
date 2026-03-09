from fastapi import FastAPI, Response, status, HTTPException
from status_pydantic_models import Student_Info


# When the API user's request is not found and yet the system does not crash, we would love to set the API response status code to something that would help the user to know what's going on.
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

def check_serial(id_: int):
    count = 0
    try:
        while count < len(var_dict):
            if var_dict[count]['serial_number'] == id_:
                break
            count += 1
        return var_dict[count]
    except IndexError:
        return None

def check_name(name: str)-> dict | None:
    count = 0
    result = ()
    try:
        while count < len(var_dict):
            if var_dict[count]['surname'] == name or var_dict[count]['first_name'] == name or var_dict[count]['other_names'] == name:
                result += var_dict[count],
            count += 1
        return result
    except IndexError:
        return None

@app.post("/post student info")
def create_post(my_post: Student_Info):
    my_post.serial_number = len(var_dict) +1
    var_dict.append(my_post.model_dump())
    full_Name= f"{my_post.surname} {my_post.first_name} {my_post.other_names}"
    raise HTTPException(status_code=status.HTTP_201_CREATED, detail=full_Name)

@app.get("/all students' info")
def get_posts():
    return var_dict

# Here we set it to a status code '404', BY

@app.get("/student id/{id_}")
def get_student_id(id_: int, my_response: Response):
    result = check_serial(id_)
    if not result:
        my_response.status_code = status.HTTP_404_NOT_FOUND
        return "This Student does not exist"
    return result

#  OR

@app.get("/student name/{name}")
def get_student_name(name: str):
    result = check_name(name)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Student as {name}")
    return result

@app.delete("/delete student info/{id_}", status_code=204)
def delete(id_: int):
    print(type(check_serial(id_)))
    if not check_serial(id_):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student does not exist")

    var_dict.remove(check_serial(id_))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.patch("/update student info/{id_}")
def update(id_: int, my_post: Student_Info):
    result = check_serial(id_)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student does not exist")
    # First convert the Student_Info class instance, 'my_post' into a proper dictionary
    my_update = my_post.model_dump()
    result['serial_number'] = id_
    result['surname'] = my_update['surname']
    result['first_name'] = my_update['first_name']
    result['other_names'] = my_update['other_names']
    result['age'] = my_update['age']
    result['residential_address'] = my_update['residential_address']

    return result

from pydantic import BaseModel

class Student_Info(BaseModel):
    serial_number: int
    surname: str
    first_name: str
    other_names: str=""
    class_: str
    age: str
    residential_address: str

class Example(BaseModel):
    message: str
    status: str
    id: int
    user: str = None


from typing import Optional
from pydantic import BaseModel

class Student_Info(BaseModel):
    serial_number: Optional[int] = 0
    surname: str
    first_name: str
    other_names: str=""
    class_: Optional[str]= ''
    age: int
    residential_address: Optional[str]= "Home"

class Update_Student_Info(BaseModel):
    surname: str

class Example(BaseModel):
    message: str
    status: str
    id: int
    user: str = None


from typing import Optional
from pydantic import BaseModel

class Student_Info(BaseModel):
    id: int
    surname: str
    first_name: str
    other_names: str=""
    age: Optional[int]
    resident_street: Optional[str]
    class_ : Optional[int]= None


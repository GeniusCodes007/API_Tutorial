from sqlalchemy.orm import Session
from fastapi import Depends
from orm_database_lesson_2.orm_database_2 import get_database


def sort_out_content(item_to_sort: str = "", db:Session= Depends(get_database)):
    print(item_to_sort)

    #db:Session= Depends(get_database)
    all_item =""
    return all_item

print(sort_out_content())

def add(a: int|float, b: int|float, c: int|float):
    print(a+ b+ c)


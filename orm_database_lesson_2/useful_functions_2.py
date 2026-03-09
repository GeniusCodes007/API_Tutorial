from sqlalchemy.orm import Session
from fastapi import Depends
from orm_database_2 import get_database
from orm_database_lesson import orm_models


def sort_out_content(item_to_sort: str = "", db:Session= Depends(get_database)):
    print(item_to_sort)

    #db:Session= Depends(get_database)
    all_item =""
    return all_item

print(sort_out_content())
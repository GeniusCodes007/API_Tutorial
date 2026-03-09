from fastapi import APIRouter


my_router = APIRouter(tags=['Root Page'])


@my_router.get("/")
def  our_welcome_page():
    return {"Hello": "World"}
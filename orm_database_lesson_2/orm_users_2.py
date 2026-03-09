
import sqlalchemy.exc
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
import orm_models_2, orm_schemas_2, orm_utils_2, orm_oauth2_2
from orm_database_2 import get_database
from pydantic import EmailStr

router = APIRouter(
    prefix="/users",
    tags=['Users']
)



#response_model=orm_schemas_2.User_Response,
@router.post("/create", status_code=status.HTTP_201_CREATED )
def create_user(user_data: orm_schemas_2.UserRegData, db:Session=Depends(get_database)):
    try:
        #Check if username or email already exists
        # If the username is found, raise Exception
        if db.query(orm_models_2.User_Reg_Data).filter(orm_models_2.User_Reg_Data.username == user_data.username).first() :
            raise HTTPException(status_code=409, detail="Username Already Registered")

        if db.query(orm_models_2.User_Reg_Data).filter(orm_models_2.User_Reg_Data.email == user_data.email).first():
            raise HTTPException(status_code=409, detail="Email Already Registered")


        # Set the value of the user_data.confirmed_password as a plain password
        user_data.confirmed_password = user_data.password

        # Set the value of the user_data.password as a hash
        user_data.password = orm_utils_2.hash_password(user_data.password)


        # Fill up the User_Reg_Data Columns
        new_user_reg_data = orm_models_2.User_Reg_Data(**user_data.model_dump())

        # Save User_Reg_Data to Database
        db.add(new_user_reg_data)
        db.commit()
        db.refresh(new_user_reg_data)


        raise HTTPException(status_code=status.HTTP_201_CREATED,
                            detail=f"Welcome aboard {new_user_reg_data.username}!!! Enjoy the New World of Technology")
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This email is already used by another user")

@router.get("/username/{username}", status_code=status.HTTP_302_FOUND, response_model=orm_schemas_2.UserAccount)
def get_user_by_username(username: str,db: Session = Depends(get_database), current_user: int=Depends(orm_oauth2_2.get_current_user)):

    user_info = db.query(orm_models_2.Personal_Data).filter(orm_models_2.Personal_Data.username == username).first()

    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User Not Found")
    # Set the fullname of the user
    my_fullname= str(orm_models_2.Personal_Data.surname) + " " + str(orm_models_2.Personal_Data.firstname) + " " + str(orm_models_2.Personal_Data.lastname)
    my_username = str(orm_models_2.Personal_Data.username)
    my_is_adult = orm_models_2.Personal_Data.is_adult
    my_email = str(orm_models_2.Personal_Data.email)

    personal_info: orm_models_2.Personal_Data = orm_models_2.Personal_Data(fullname=my_fullname,email=my_email, username=my_username,is_adult=my_is_adult)
    return personal_info

@router.get("/email/{user_email}", status_code=status.HTTP_302_FOUND, response_model=orm_schemas_2.UserAccount)
def get_user_by_email(user_email: EmailStr,db: Session = Depends(get_database), current_user: int=Depends(orm_oauth2_2.get_current_user)):

    user_info = db.query(orm_models_2.User_Reg_Data).filter(orm_models_2.User_Reg_Data.email == user_email).first()
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Email Not Found")
    return user_info

@router.patch("/{post_title}", status_code=status.HTTP_202_ACCEPTED, response_model=orm_schemas_2.UpdatePost)
async def update_post(updated_post_schema: orm_schemas_2.UpdatePost, post_title: str ,db: Session = Depends(get_database), current_user: int=Depends(orm_oauth2_2.get_current_user)):

    post_in_search = None

    # Search all possible posts with title, post_title
    all_users_posts = db.query(orm_models_2.User_Posts).filter(orm_models_2.User_Posts.postTitle == post_title).all()

    # If None, raise Exception
    if not all_users_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posts With Title, {post_title}, Not Found")

    # If it should be, find the post made by the user
    for user_post in all_users_posts:
        if user_post.email == updated_post_schema.email and user_post.username == updated_post_schema.username:
            post_in_search = user_post

    # If there is no post by user
    if not post_in_search:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Post With Title, {post_title} Found In Your Name")


    updated_post_schema.postContent = str(post_in_search.postContent) + str(updated_post_schema.postContent)



    # Unpack
    db.query(orm_models_2.User_Posts).where(
        orm_models_2.User_Posts.postTitle == post_title and orm_models_2.User_Posts.username == post_in_search.username).update(
        updated_post_schema.model_dump(), synchronize_session=False)
    # Save changes made
    db.commit()

    return post_in_search

@router.put("/{post_title}", status_code=status.HTTP_202_ACCEPTED, response_model=orm_schemas_2.UpdatePost)
async def change_entire_post_content(updated_post_schema: orm_schemas_2.UpdatePost, post_title: str ,db: Session = Depends(get_database), current_user: int=Depends(orm_oauth2_2.get_current_user)):

    post_in_search = None

    # Search all possible posts with title, post_title
    all_users_posts = db.query(orm_models_2.User_Posts).filter(orm_models_2.User_Posts.postTitle == post_title).all()

    # If None, raise Exception
    if not all_users_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posts With Title, {post_title}, Not Found")

    # If it should be, find the post made by the user
    for user_post in all_users_posts:
        if user_post.email == updated_post_schema.email and user_post.username == updated_post_schema.username:
            post_in_search = user_post

    # If there is no post by user
    if not post_in_search:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No Post With Title, {post_title} Found In Your Name")


    # Unpack
    db.query(orm_models_2.User_Posts).where(
        orm_models_2.User_Posts.postTitle == post_title and orm_models_2.User_Posts.username == post_in_search.username).update(
        updated_post_schema.model_dump(), synchronize_session=False)
    # Save changes made
    db.commit()

    return post_in_search
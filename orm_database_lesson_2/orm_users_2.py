
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
def create_user(user_data: orm_schemas_2.CreateUser, db:Session=Depends(get_database)):
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


        # Create and fill up the User_Reg_Data Columns
        new_user_reg_data = orm_models_2.User_Reg_Data(username=user_data.username, email=user_data.email,
                                                       password=user_data.password, confirmed_password=user_data.confirmed_password)

        # Save User_Reg_Data to Database
        db.add(new_user_reg_data)

        # Create and fill up the User_Personal_Data Columns
        new_personal_data = orm_models_2.Personal_Data(username=user_data.username, email=user_data.email,
                                                       surname=user_data.surname, firstname=user_data.firstname,
                                                       lastname=user_data.lastname, is_adult=user_data.is_adult)
        db.add(new_personal_data)

        db.commit()
        db.refresh(new_user_reg_data)

        raise HTTPException(status_code=status.HTTP_201_CREATED,
                            detail=f"Welcome aboard {new_user_reg_data.username}!!! Enjoy the New World of Technology")
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="This email is already used by another user")

@router.get("/username/{username_or_email}", status_code=status.HTTP_302_FOUND, response_model=orm_schemas_2.UserAccount)
def get_user(username_or_email: str|EmailStr, db: Session = Depends(get_database), current_user: int=Depends(orm_oauth2_2.get_current_user)):

    # Check if the user is logged in
    if not current_user:
        raise   HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="Login To Gain Access")

    # Find record of user
    user_info = db.query(orm_models_2.Personal_Data).filter(orm_models_2.Personal_Data.username == username_or_email or orm_models_2.Personal_Data.email == username_or_email).first()

    # If None, raise Exception
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Details For {username_or_email} Not Found")

    # Create an instance of UserAccount

    # Set the attribute values for the UserAccount, to display the account info
    my_fullname= str(orm_models_2.Personal_Data.surname) + " " + str(orm_models_2.Personal_Data.firstname) + " " + str(orm_models_2.Personal_Data.lastname)
    my_username = str(orm_models_2.Personal_Data.username)
    my_email = orm_models_2.Personal_Data.email


    personal_info: orm_schemas_2.UserAccount = orm_schemas_2.UserAccount(fullname=my_fullname,email=my_email, username=my_username)
    return personal_info

@router.patch("/{post_title}", status_code=status.HTTP_202_ACCEPTED, response_model=orm_schemas_2.UpdatePost)
async def update_post(updated_post_schema: orm_schemas_2.UpdatePost, post_title: str ,db: Session = Depends(get_database), current_user: int=Depends(orm_oauth2_2.get_current_user)):

    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Login To Gain Access")

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

    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Login To Gain Access")

    post_in_search = None

    # Search all possible posts with title, post_title
    all_users_posts = db.query(orm_models_2.User_Posts).filter(orm_models_2.User_Posts.postTitle == post_title).all()

    # If None, raise Exception
    if not all_users_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Posts With Title, {post_title}, By You Not Found")

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

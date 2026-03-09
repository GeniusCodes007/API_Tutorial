import psycopg2
import fastapi.exceptions as my_error
import sqlalchemy.exc
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
import orm_models
import orm_schemas
import orm_database
import orm_oauth2

#from orm_database import get_database

router = APIRouter(
    prefix="/posts",
    tags=['Posts'],
)


@router.post("/create" , status_code=status.HTTP_201_CREATED ,)# response_model=orm_schemas.CreatePost, )
def create_post(post_schema: orm_schemas.CreatePost, db: Session = Depends(orm_database.get_database), current_user: int=Depends(orm_oauth2.get_current_user)):
    try:

        # Search by Email
        user_by_email = db.query(orm_models.User_Reg_Data).filter(orm_models.User_Reg_Data.email == post_schema.email).first()
    
        # Search by Username
        user_by_username = db.query(orm_models.User_Reg_Data).filter(orm_models.User_Reg_Data.username == post_schema.username).first()
    
        # if invalid, raise exception
        if user_by_email :
            work_with = user_by_email
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You may need to login first")
    
        # if invalid, raise exception
        if user_by_username :
            work_with = user_by_username
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Do Not Formulate Username, If Not Signed Up")
    
    
        # After User is successfully validated
    
        # Check if the user's newly posted postTitle already exists by the user himself
        find_post_title = db.query(orm_models.User_Posts).filter(orm_models.User_Posts.postTitle == post_schema.postTitle).all()
        for x in find_post_title:
            if x.username == post_schema.username or x.email == post_schema.email:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"Post With Title: {post_schema.postTitle} By You Already Exists!!!  Would You Prefer To Update This Post???")
    
    
        # Set the value for the foreign key 'postUserId'
        post_schema.postUserId = work_with.id
    
        # Unpack the CreatePost schema into User_Posts model
        new_post_data = orm_models.User_Posts(**post_schema.model_dump())
    
        # Add new_post_data to the database
        db.add(new_post_data)
        # Commit changes to the database
        db.commit()
        # Refresh data database to see changes made
        db.refresh(new_post_data)
    
        return new_post_data
    except sqlalchemy.exc.IntegrityError :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,)


@router.get("/{post_title}", status_code=status.HTTP_200_OK,)# response_model=orm_schemas.CreatePost)
def get_post_info(post_title: str, db: Session = Depends(orm_database.get_database), current_user: int=Depends(orm_oauth2.get_current_user)):
    # Check if post of post_title by user exists
    info_post = db.query(orm_models.User_Posts).filter(orm_models.User_Posts.postTitle == post_title).all()

    # If not existent, raise Exception
    if not info_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post Not Found!!! Would You Love To Be The First To Create This Post???")

    return info_post


@router.delete("/{post_title}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_title: str, db: Session = Depends(orm_database.get_database), current_user: int=Depends(orm_oauth2.get_current_user)):
    post_to_delete = db.query(orm_models.User_Posts).filter(orm_models.User_Posts.postTitle == post_title)

    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post Not Found")
    post_to_delete.delete(synchronize_session=False)
    db.commit()




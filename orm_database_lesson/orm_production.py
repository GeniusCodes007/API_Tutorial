from typing import List
from pydantic import EmailStr
from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
import orm_models, orm_schemas
from orm_database import get_database

router = APIRouter(
    prefix="/prod",
    tags=['Production']
)



@router.get("/user reg data", status_code=status.HTTP_200_OK, response_model=List[orm_schemas.UserRegData])
def get_all_user_reg_data_info(db: Session = Depends(get_database)):
    user_reg_data = db.query(orm_models.User_Reg_Data).order_by(orm_models.User_Reg_Data.id).all()
    return user_reg_data


@router.get("/personal data", status_code=status.HTTP_200_OK, response_model=List[orm_schemas.UserPersonalData])
def get_all_personal_data_info(db: Session = Depends(get_database)):
    personal_data =db.query(orm_models.Personal_Data).order_by(orm_models.Personal_Data.id).all()
    return personal_data


@router.get("/user posts", status_code=status.HTTP_200_OK, response_model=List[orm_schemas.UserPosts])
def get_all_user_posts_info(db: Session = Depends(get_database)):
    user_posts = db.query(orm_models.User_Posts).order_by(orm_models.User_Posts.id).all()
    return user_posts


# Delete by ID
@router.delete("/{username_or_email}/{post_title}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(username_or_email: str|EmailStr, post_title: str, db: Session = Depends(get_database)):
    work_with = None
    # Find all posts with title, post_title
    all_posts = db.query(orm_models.User_Posts).filter(orm_models.User_Posts.postTitle == post_title).all()

    # If no post is found
    if not all_posts:
        raise HTTPException(status_code=404, detail="No Posts Found")

    for post in all_posts:
        if post.username == username_or_email:
            work_with = post
        if post.email == username_or_email:
            work_with = post

    # If no post belongs to username_or_email
    if not work_with:
        raise HTTPException(status_code=404, detail=f"No Post With Title, {post_title}, Found In {username_or_email}'s Name")

    db.delete(work_with)
    db.commit()


from typing import List
from pydantic import EmailStr
from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.orm import Session
import orm_database_lesson_2.orm_models_2, orm_database_lesson_2.orm_schemas_2
from orm_database_lesson_2.orm_database_2 import get_database

router = APIRouter(
    prefix="/prod",
    tags=['Production']
)



@router.get("/user reg data", status_code=status.HTTP_200_OK, response_model=List[orm_database_lesson_2.orm_schemas_2.UserRegData])
def get_all_user_reg_data_info(db: Session = Depends(get_database)):
    user_reg_data = db.query(orm_database_lesson_2.orm_models_2.User_Reg_Data).order_by(orm_database_lesson_2.orm_models_2.User_Reg_Data.id).all()
    return user_reg_data


@router.get("/personal data", status_code=status.HTTP_200_OK, response_model=List[orm_database_lesson_2.orm_schemas_2.UserPersonalData])
def get_all_personal_data_info(db: Session = Depends(get_database)):
    personal_data =db.query(orm_database_lesson_2.orm_models_2.Personal_Data).order_by(orm_database_lesson_2.orm_models_2.Personal_Data.id).all()
    return personal_data


@router.get("/user posts", status_code=status.HTTP_200_OK, response_model=List[orm_database_lesson_2.orm_schemas_2.UserPosts])
def get_all_user_posts_info(db: Session = Depends(get_database)):
    user_posts = db.query(orm_database_lesson_2.orm_models_2.User_Posts).order_by(orm_database_lesson_2.orm_models_2.User_Posts.id).all()
    return user_posts


# Delete by ID
@router.delete("/{username_or_email}/{post_title}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(username_or_email: str|EmailStr, post_title: str, db: Session = Depends(get_database)):
    work_with = None
    # Find all posts with title, post_title
    all_posts = db.query(orm_database_lesson_2.orm_models_2.User_Posts).filter(orm_database_lesson_2.orm_models_2.User_Posts.postTitle == post_title).all()

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

@router.delete("/{username_or_email}", )#status_code=status.HTTP_200_OK, response_model=List[orm_schemas_2.UserRegData])
def get_all_user_reg_data_info(username_or_email: str|EmailStr, db: Session = Depends(get_database)):

    user_reg_data = db.query(orm_database_lesson_2.orm_models_2.User_Reg_Data).filter(orm_database_lesson_2.orm_models_2.User_Reg_Data.username == username_or_email)
    user_reg_data_by_email = db.query(orm_database_lesson_2.orm_models_2.User_Reg_Data).filter(orm_database_lesson_2.orm_models_2.User_Reg_Data.email == username_or_email)

    if user_reg_data.first():
        user_reg_data.delete(synchronize_session=False)
        db.commit()
    if user_reg_data_by_email.first():
        user_reg_data_by_email.delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {username_or_email} not found")

@router.get("/post votes", status_code=status.HTTP_200_OK)
def get_all_post_votes(db: Session = Depends(get_database)):
    try:
        all_votes = db.query(orm_database_lesson_2.orm_models_2.Post_Votes).all()
        return all_votes
    except Exception as e:
        return e

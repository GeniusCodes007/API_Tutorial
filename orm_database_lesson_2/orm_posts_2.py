
import sqlalchemy.exc
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
import orm_database_lesson_2.orm_models_2
import orm_database_lesson_2.orm_schemas_2
import orm_database_lesson_2.orm_database_2
import orm_database_lesson_2.orm_oauth2_2

#from orm_database_2 import get_database

router = APIRouter(
    prefix="/posts",
    tags=['Posts'],
)


@router.post("/create" , status_code=status.HTTP_201_CREATED , response_model=orm_database_lesson_2.orm_schemas_2.CreatePost, )
def create_post(post_schema: orm_database_lesson_2.orm_schemas_2.CreatePost, db: Session = Depends(orm_database_lesson_2.orm_database_2.get_database), current_user: int=Depends(orm_database_lesson_2.orm_oauth2_2.get_current_user),):
    try:
        if not current_user:
            return "Not Authorized", current_user
        # If the username is registered
        if current_user.username != post_schema.username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Are You Logged In?",)

        # Also, check if the email is registered
        if current_user.email !=post_schema.email:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Do You Own The Account?",)

        # Find all posts with the post title the user wants to create
        possible_posts=db.query(orm_database_lesson_2.orm_models_2.User_Posts).filter(orm_database_lesson_2.orm_models_2.User_Posts.postTitle == post_schema.postTitle).all()

        # If they exist ...
        if possible_posts:

            # Find if the user has already created a post with that title
            for single_post in possible_posts:
                # If found, raise Exception
                if single_post.postUserId == current_user.id:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                        detail="This Post Already Exists By You!!! Consider Updating This Post",)

        new_post =orm_database_lesson_2.orm_models_2.User_Posts(postUserId=current_user.id, username=post_schema.username, email=post_schema.email,
                                          postTitle=post_schema.postTitle, postContent=post_schema.postContent)

        db.add(new_post)
        db.flush()


        # Create Post Vote

        # Set attribute-values for Post Vote
        p_id = int(new_post.id)
        u_id = int(new_post.postUserId)
        v_post_title = post_schema.postTitle
        v_author_email= post_schema.email
        v_author_username=post_schema.username

        create_vote = orm_database_lesson_2.orm_models_2.Post_Votes( post_id=p_id, user_id=u_id, vote_postTitle=v_post_title,
                                            vote_Author_Email=v_author_email, vote_Author_Username=v_author_username)


        db.add(create_vote)
        #db.flush()
        db.commit()


        return new_post
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Why are you duplicating???")


@router.get("/{post_title}", status_code=status.HTTP_200_OK,)# response_model=orm_schemas_2.CreatePost)
def get_post_info(post_title: str, db: Session = Depends(orm_database_lesson_2.orm_database_2.get_database), current_user: int=Depends(orm_database_lesson_2.orm_oauth2_2.get_current_user)):

    # Check if user is registered
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not Authorized", )

    # Check if post of post_title by user exists
    info_post = db.query(orm_database_lesson_2.orm_models_2.User_Posts).filter(orm_database_lesson_2.orm_models_2.User_Posts.postTitle == post_title).all()

    # If not existent, raise Exception
    if not info_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post Not Found!!! Would You Love To Be The First To Create This Post???")

    return info_post


@router.delete("/{post_title}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_title: str, db: Session = Depends(orm_database_lesson_2.orm_database_2.get_database), current_user: int=Depends(orm_database_lesson_2.orm_oauth2_2.get_current_user)):
    # Check if user is registered
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not Authorized", )

    post_to_delete = db.query(orm_database_lesson_2.orm_models_2.User_Posts).filter(orm_database_lesson_2.orm_models_2.User_Posts.postTitle == post_title and orm_database_lesson_2.orm_models_2.User_Posts.postUserId == current_user.id).first()

    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post Not Found")
    post_to_delete.delete(synchronize_session=False)
    db.commit()




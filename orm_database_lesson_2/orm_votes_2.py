from fastapi import APIRouter, Depends, HTTPException, status
import orm_schemas_2
#from orm_models import Post_Votes
from orm_database_2 import get_database
from sqlalchemy.orm import Session
import orm_oauth2_2
import orm_models_2



router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
def vote_(vote: orm_schemas_2.Vote, db: Session = Depends(get_database), current_user: int= Depends(orm_oauth2_2.get_current_user)):

    user_post_to_find = None
    vote_post_to_find = None

    # Check if the user is registered
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="You're not an authentic user")

    # Find all post_votes with the required post_title
    find_all_votes = db.query(orm_models_2.Post_Votes).filter(orm_models_2.Post_Votes.vote_postTitle == vote.post_title).all()

    # Find all posts with the required post_title
    find_all_posts= db.query(orm_models_2.User_Posts).filter(orm_models_2.User_Posts.postTitle == vote.post_title).all()

    # Narrow down search to find the particular vote
    for vote_post in find_all_votes:
        if vote_post.vote_Author_Username == vote.post_author_username_or_email or vote_post.vote_Author_Email == vote.post_author_username_or_email:
            vote_post_to_find = vote_post

    # Narrow down search to find particular post
    for post in find_all_posts:
        if post.username == vote.post_author_username_or_email or post.email == vote.post_author_username_or_email:
            user_post_to_find = post

    # If no post exists, then no post_vote for the post, therefore raise Exception
    if not user_post_to_find:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No Such Post Found")
    # If the user votes up,
    if vote.is_up_vote:
        # Check if the user's has once voted down
        if current_user.username in vote_post_to_find.down_votes_users or current_user.email in vote_post_to_find.down_votes_users:
            # If so,
            # Remove the user's username from the down voters list for that post
            vote_post_to_find.down_votes_users.remove(current_user.username)
            # Subtract a point for undoing down vote
            user_post_to_find.down_votes = user_post_to_find.down_votes - 1
        # Add the user's username to the up voters list for that post
        vote_post_to_find.up_votes_users.append(current_user.username)
        # Add a point for doing up vote
        user_post_to_find.up_votes = user_post_to_find.up_votes + 1
        print("Up Vote")

    # If the user votes down,
    if not vote.is_up_vote:
        # Check if the user's has once voted up
        if current_user.username in vote_post_to_find.up_votes_users or current_user.email in vote_post_to_find.up_votes_users:
            # If so,
            # Remove the user's username from the up voters list for that post
            vote_post_to_find.up_votes_users.remove(current_user.username)
            # Subtract a point for undoing up vote
            user_post_to_find.up_votes = user_post_to_find.up_votes - 1
            # Add the user's username to the down voters list for that post
        vote_post_to_find.down_votes_users.append(current_user.username)
        # Add a point for doing down vote
        user_post_to_find.down_votes = user_post_to_find.down_votes + 1
        print("Down Vote")

    # Check to make sure a user cannot vote themselves
    if current_user.email == vote.post_author_username_or_email or current_user.username == vote.post_author_username_or_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"{vote.post_author_username_or_email}, You Cannot Vote Yourself")

    # Unpack items
    db.query(orm_models_2.Post_Votes).filter(orm_models_2.Post_Votes.vote_postTitle == vote.post_title and (orm_models_2.Post_Votes.vote_Author_Email == vote.post_author_username_or_email or orm_models_2.Post_Votes.vote_Author_Username == vote.post_author_username_or_email)).update({
        "post_id" : int(user_post_to_find.id),
    "user_id" : int(vote_post_to_find.user_id),
    "vote_postTitle": vote_post_to_find.vote_postTitle,
    "vote_Author_Email" : vote_post_to_find.vote_Author_Email,
    "vote_Author_Username" : vote_post_to_find.vote_Author_Email,
    "up_votes_users" : vote_post_to_find.up_votes_users,
    "down_votes_users": vote_post_to_find.down_votes_users
    }, synchronize_session=False)

    db.query(orm_models_2.User_Posts).filter(orm_models_2.User_Posts.postTitle == vote.post_title and (orm_models_2.User_Posts.username == vote.post_author_username_or_email or orm_models_2.User_Posts.email == vote.post_author_username_or_email)).update({
        "postUserId": user_post_to_find.postUserId,
    "email": user_post_to_find.email,
    "username": user_post_to_find.username,
    "postTitle": user_post_to_find.postTitle,
    "postContent" : user_post_to_find.postContent,
    "up_votes" : user_post_to_find.up_votes,
    "down_votes": user_post_to_find.down_votes
    }, synchronize_session=False)

    db.commit()

    return f"Great!!! {current_user.username} Thanks for Your Vote"

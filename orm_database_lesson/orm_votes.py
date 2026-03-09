from fastapi import APIRouter, Depends, HTTPException, status
from orm_schemas import Vote#, VotingResponse
#from orm_models import Post_Votes
from orm_database import get_database
from sqlalchemy.orm import Session
from orm_oauth2 import oauth2_scheme
import orm_models



router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_(vote: Vote, db: Session = Depends(get_database), current_user: int= Depends(oauth2_scheme)):
    vote_query = db.query(orm_models.Vote).filter(orm_models.Vote.vote_posts_id == vote.post_id,
                                                  orm_models.Vote.vote_users_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_423_LOCKED,
                                detail="You can't vote more than once")
        model_vote = orm_models.Vote(votes_post_id=vote.post_id, votes_users_id=current_user.id)
        db.add(model_vote)
        db.commit()
        return "Thanks For Your Vote"
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No vote found")
        vote_query.delete(synchronize_session=False)
        return "Thanks For Your Vote"


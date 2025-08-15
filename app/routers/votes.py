from fastapi import APIRouter, Response, Depends, HTTPException,status
from app import schemas,models,database, auth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/votes",
    tags= ['Votes']
)

@router.post('/',status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Votes,db : Session = Depends(database.get_db), current_user : int= Depends(auth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {vote.post_id} does not exist.")

    vote_query = db.query(models.votes).filter(models.votes.post_id == vote.post_id,models.votes.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'Successfully added vote'}
    
    else:
        if found_vote:
            vote_query.delete(synchronize_session = False)
            db.commit()
            return {'message': 'Successfully deleted vote'}
        
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "you haven't voted yet!")

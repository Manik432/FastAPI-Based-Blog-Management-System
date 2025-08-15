from app import auth2, models,schemas
from app.database import get_db
from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix = '/posts',
    tags = ['Posts']  # for grouping based on the name 'eg. posts' in the FASTAPI documentation @serverip/docs
)

@router.get("/" ,response_model = list[schemas.postOut])
def get_post(db: Session=Depends(get_db), curr_user: int= Depends(auth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()  #.query is making an SQL query internally and .all is running that query to get the result
    
    posts = db.query(models.Post,func.count(models.votes.post_id).label("votes")).join(models.votes, models.votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    if posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nothing to Retrieve from the database.")  
    
    return posts


@router.post("/",status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post: schemas.postcreate,db: Session=Depends(get_db), curr_user: int= Depends(auth2.get_current_user)):
    
    new_post = models.Post(owner_id = curr_user.id, **post.model_dump())   # here used **post.model_dump() as it will convert all the fields of the model into dictionary 
                                                    #and will assign the given values to there respective fields and will work the same as in the 
                                                    # SQL query as the following:  (title=post.title,caption = post.caption,content = post.content)
    
    print(curr_user.email)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # .refresh() to return the newly created entry

    return new_post


@router.get('/{id}', response_model = schemas.postOut)
def getapost(id : int,db: Session=Depends(get_db), curr_user: int= Depends(auth2.get_current_user)):

    #found_post = db.query(models.Post).filter(models.Post.id == id).first()
    found_post = db.query(models.Post,func.count(models.votes.post_id).label("votes")).join(models.votes, models.votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
     
    if found_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} id is not present in the database.")
    
    # if found_post.owner_id != curr_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform the requested action.")

    return found_post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session=Depends(get_db), curr_user: int= Depends(auth2.get_current_user)):

    deleting_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleting_post = deleting_post_query.first()

    if deleting_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id {id} does not exist.")
    
    if deleting_post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform the requested action.")
    
    deleting_post_query.delete(synchronize_session = False)  #synchronize_session usage -> When SQLAlchemy deletes objects 
                                                            #using .delete() directly on a query (without loading them into memory), 
                                                            # it needs to synchronize the session — meaning it has to keep the session's in-memory state in sync 
                                                            # with what changed in the DB.
    db.commit()

    return {"message":f"The post with id {id} has been deleted."}


@router.put("/{id}", response_model = schemas.Post)
def update_post(id:int,post :schemas.postcreate,db: Session = Depends(get_db), curr_user: int = Depends(auth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    retrieved_post = post_query.first()

    if retrieved_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id: {id} is not assciated with any of the entries in the database.")

    if retrieved_post.owner_id != curr_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not Authorized to perform the requested action.")
    
    post_query.update(post.model_dump(),synchronize_session = False)  #synchronize_session usage -> When SQLAlchemy deletes objects 
                                                            #using .delete() directly on a query (without loading them into memory), 
                                                            # it needs to synchronize the session — meaning it has to keep the session's in-memory state in sync 
                                                            # with what changed in the DB.

    db.commit()

    return post_query.first()
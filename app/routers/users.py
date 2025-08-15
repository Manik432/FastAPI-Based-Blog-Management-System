from app import models,schemas,utils
from app.database import get_db
from fastapi import FastAPI,Response,status,HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = '/users',
    tags = ['Users']
)

@router.post("/",status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_user(user:schemas.UserCreate, db: Session=Depends(get_db)):


    # Hash the password - user.password

    hashed_password = utils.hashing(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.model_dump())   # here used **user.model_dump() as it will convert all the fields of the model into dictionary 
                                                    #and will assign the given values to there respective fields and will work the same as in the 
                                                    # SQL query as the following:  (email=user.email,password = user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model= schemas.UserOut)
def getUser(id:int, db: Session=Depends(get_db)):

    found_user = db.query(models.Users).filter(models.Users.id == id).first()

    if not found_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{id} id is not present in the database.")  

    return found_user
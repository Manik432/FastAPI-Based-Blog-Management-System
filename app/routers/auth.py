from fastapi import APIRouter, Response, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import session
from app import database, schemas, models, utils, auth2

router = APIRouter(
    tags= ['Authentication']
)

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db : session = Depends(database.get_db)):

    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail= 'Invalid Credentials')
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail= 'Invalid Credentials')
    
    # create a token

    AccessToken = auth2.createToken(data={"user_id": user.id})

    return {'access_token': AccessToken, "token_type": "Bearer Token"}
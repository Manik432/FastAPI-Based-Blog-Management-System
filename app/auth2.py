from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app import schemas, database, models
from fastapi import Depends,HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import session
from app.config import settings

Oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = settings.secret_key
Algorithm = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def createToken(data : dict):
    to_encode = data.copy()

    expireTime = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': int(expireTime.timestamp())})

    encodedData = jwt.encode(to_encode,SECRET_KEY, algorithm=Algorithm)

    return encodedData


def verifyToken(token: str,credentials_exception):

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[Algorithm])
        user_id  = payload.get("user_id")

        if not user_id:
            raise credentials_exception
        
        token_data = schemas.TokenData(id = user_id)

    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(Oauth2_scheme), db: session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={'WWW-Authenticate:': 'Bearer'})

    token = verifyToken(token, credentials_exception)

    user = db.query(models.Users).filter(models.Users.id ==  token.id).first()
    
    return user
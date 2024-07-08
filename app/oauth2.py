from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from . import schemas, models
from sqlalchemy.orm import Session
from .database import get_db
from fastapi import Depends, status, HTTPException
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes



def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = decoded_jwt.get("user_id")

        if not id:
            raise credential_exception
        token_data = schemas.TokenData(id=id)

    except ExpiredSignatureError:
        print("Token has expired.")
        raise credential_exception

    except JWTError:
        raise credential_exception

    return token_data


# def verify_access_token(token: str, credential_exception):
#     decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

#     try:
#         id = decoded_jwt.get("user_id")

#         if not id:
#             raise credential_exception
#         token_data = schemas.TokenData(id=id)
    
#     except ExpiredSignatureError:
#         # Handle expired token specifically
#         raise credential_exception
    
#     except JWTError:
#         raise credential_exception
    
#     return token_data
    
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"www-Authenticate":"Bearer"})

    token = verify_access_token(token, credential_exception)
    current_user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return current_user
    

from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2
from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.email == user_credentials.username)

    if not user_query.first():
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
    
    pwd_match = utils.verify(user_credentials.password, user_query.first().password)

    if not pwd_match:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
    user = user_query.first()
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}



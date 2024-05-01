from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from .. import models, schemas, utils
from ..database import get_db


router = APIRouter( prefix="/users", tags=['User'])


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #password hashing
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", status_code = status.HTTP_201_CREATED, response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)

    if not user_query.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"user with id:{id} was not found")
    
    return user_query.first()

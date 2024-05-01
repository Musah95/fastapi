from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import oauth2
from ..database import get_db
from fastapi import Depends, status, HTTPException, APIRouter
from .. import models, schemas

router = APIRouter( prefix="/posts", tags=['Posts'])



@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=List[schemas.PostVotes])
# @router.get("/")
def get_posts(db:Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user), lim:int=5, skip:int=0, search:Optional[str]=""):

    # posts_query = db.query(models.Post)
    # .query(models.Post, func.count(models.Vote.post_id).label("votes"))
    # .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
    # .group_by(models.Post.id)
    # .filter(models.Post.title.contains(search)).limit(lim).offset(skip)    # .filter(models.Post.owner_id == current_user.id)
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(lim).offset(skip)

    return post_query.all()


@router.get("/{id}", response_model=schemas.PostVotes)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # post_query = db.query(models.Post).filter(models.Post.id == id)
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)
    post = post_query.first()

    if not post: 
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
        # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"Unauthorized request")
    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"Unauthorized request")
    
    post_query.delete(synchronize_session=False)
    db.commit()


@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"Unauthorized request")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post


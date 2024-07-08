from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class UserBase(BaseModel):
    username : str

class PostBase(BaseModel):
    title : str
    content : str
    user_id :int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.post('/users/', status_code= status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()

@app.get('/users/{user_id}',status_code=status.HTTP_200_OK)
async def read_user(user_id:int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='user not found')
    return user

# create post

@app.post('/post/',status_code= status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()

#get specific post

@app.get('/post/{user_post}', status_code= status.HTTP_200_OK)
async def read_post(user_post: int, db: db_dependency ):
    post = db.query(models.Post).filter(models.Post.id == user_post).first()
    if post is None:
        raise HTTPException(status_code=404, detail= 'post not found')
    return post

# delete post

@app.delete('/post/{post_id}', status_code=status.HTTP_200_OK)
async def post_delete(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail=' post not found')
    db.delete(post)
    db.commit()
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import models
from database import engine, sessionlocal
from models import PostCreate, PostResponse,Base
from schema import Post
import schema

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to my API"}

@app.get("/getall", response_model=List[PostResponse])
def get_data(db: Session = Depends(get_db)):
    posts = db.query(schema.Post).all()
    return posts

@app.post("/create_new", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_new(post: PostCreate, db: Session = Depends(get_db)):
    new_post = schema.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/getbyid/{id}", response_model=PostResponse)
def get_byid(id: int, db: Session = Depends(get_db)):
    post = db.query(schema.Post).filter(schema.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id not found")
    return post

@app.delete("/deletebyid/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_byid(id: int, db: Session = Depends(get_db)):
    delete_post = db.query(schema.Post).filter(schema.Post.id == id).first()
    if not delete_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id not found")
    db.delete(delete_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/update/{id}", response_model=PostResponse)
def update_id(id: int, post: PostCreate, db: Session = Depends(get_db)):
    update_post = db.query(schema.Post).filter(schema.Post.id == id).first()
    if not update_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id not found")
    for key, value in post.dict().items():
        setattr(update_post, key, value)
    db.commit()
    db.refresh(update_post)
    return update_post
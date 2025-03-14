from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
import crud
import dependencies
from database import SessionLocal, engine, init_db
from fastapi.responses import JSONResponse
from aiocache import Cache


init_db()
app = FastAPI()


models.Base.metadata.create_all(bind=engine)

cache = Cache.from_url("memory://")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup")
async def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.signup_user(db=db, user=user)

@app.post("/login")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return crud.login_user(db=db, user=user)

@app.post("/add_post")
async def add_post(post: schemas.PostCreate, token: str, db: Session = Depends(get_db)):
    return crud.add_post(db=db, post=post, token=token)

@app.get("/get_posts")
async def get_posts(token: str, db: Session = Depends(get_db)):
    return crud.get_posts(db=db, token=token)

@app.delete("/delete_post/{post_id}")
async def delete_post(post_id: int, token: str, db: Session = Depends(get_db)):
    return crud.delete_post(db=db, post_id=post_id, token=token)

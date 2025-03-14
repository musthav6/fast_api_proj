from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
import schemas
from fastapi import HTTPException, status
from passlib.context import CryptContext
from uuid import uuid4
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "secretkey"
ALGORITHM = "HS256"

def hash_password(password: str):
    return pwd_context.hash(password)

def signup_user(db: Session, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User created successfully"}

def login_user(db: Session, user: schemas.UserLogin):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = jwt.encode({"user_id": db_user.id}, SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token}

def add_post(db: Session, post: schemas.PostCreate, token: str):
    user_id = decode_token(token)
    db_post = models.Post(text=post.text, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {"postID": db_post.id}

def get_posts(db: Session, token: str):
    user_id = decode_token(token)
    posts = db.query(models.Post).filter(models.Post.user_id == user_id).all()
    return posts

def delete_post(db: Session, post_id: int, token: str):
    user_id = decode_token(token)
    post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.user_id == user_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"msg": "Post deleted"}

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

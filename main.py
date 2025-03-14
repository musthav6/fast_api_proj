from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas
import crud
from cashe import get_from_cache, cache_to_memory
from database import SessionLocal, engine, init_db



init_db()
app = FastAPI()


models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup")
async def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    This endpoint registers a new user by accepting an email and password.

    Parameters:
    - email (str): User's email address.
    - password (str): User's password.

    Returns:
    - A token (JWT or random string) for the registered user.
    - 400 Bad Request if email or password is invalid.
    """
    return crud.signup_user(db=db, user=user)

@app.post("/login")
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    This endpoint authenticates a user by email and password.

    Parameters:
    - email (str): User's email address.
    - password (str): User's password.

    Returns:
    - A token (JWT or random string) upon successful login.
    - 401 Unauthorized if credentials are incorrect.
    """
    return crud.login_user(db=db, user=user)

@app.post("/add_post")
async def add_post(post: schemas.PostCreate, token: str, db: Session = Depends(get_db)):
    """
    Adds a new post for the authenticated user.

    Parameters:
    - token (str): User's authentication token.
    - text (str): The content of the post.

    Returns:
    - postID (str) of the newly created post.
    - 400 Bad Request if validation fails (payload exceeds 1 MB or token is invalid).
    """
    return crud.add_post(db=db, post=post, token=token)

@app.get("/get_posts")
async def get_posts(token: str, db: Session = Depends(get_db)):
    """
    Retrieves all posts for the authenticated user.

    Parameters:
    - token (str): User's authentication token.

    Returns:
    - List of posts made by the user.
    - 401 Unauthorized if token is invalid or missing.
    """
    user_id = crud.decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    cached_posts = get_from_cache(user_id)
    if cached_posts:
        return cached_posts

    posts = crud.get_posts(db=db,token=token)
    cache_to_memory(user_id, posts)
    return posts

@app.delete("/delete_post/{post_id}")
async def delete_post(post_id: int, token: str, db: Session = Depends(get_db)):
    """
    Deletes a specific post identified by postID for the authenticated user.

    Parameters:
    - postID (int): The ID of the post to be deleted.
    - token (str): User's authentication token.

    Returns:
    - 200 OK if post is successfully deleted.
    - 401 Unauthorized if token is invalid or missing.
    """
    return crud.delete_post(db=db, post_id=post_id, token=token)

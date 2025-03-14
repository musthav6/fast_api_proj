# API Documentation for User Posts Management

This FastAPI application provides endpoints for user authentication, managing posts, and caching data. It ensures efficient database calls, request validation, and in-memory caching to improve performance.

---

## Endpoints Overview:

### 1. Signup Endpoint
- **POST /signup**
- **Request body:**
    ```json
    {
      "email": "user@example.com",
      "password": "password123"
    }
    ```
- **Response:**
  Returns a token for the user (JWT or random string).
    - **Success:** 200 OK
    - **Failure:** 400 Bad Request (if validation fails)

### 2. Login Endpoint
- **POST /login**
- **Request body:**
    ```json
    {
      "email": "user@example.com",
      "password": "password123"
    }
    ```
- **Response:**
  Returns a token upon successful login.
    - **Success:** 200 OK
    - **Failure:** 401 Unauthorized (if credentials are incorrect)

### 3. AddPost Endpoint
- **POST /add_post**
- **Request body:**
    ```json
    {
      "text": "My first post!",
      "token": "user_token"
    }
    ```
- **Validation:**
    - Ensure the payload does not exceed 1 MB.
- **Response:**
    - Returns the `postID` on successful post creation.
    - Returns an error for invalid or missing token.
    - Uses token-based authentication.

### 4. GetPosts Endpoint
- **GET /get_posts**
- **Headers:**
    ```json
    {
      "token": "user_token"
    }
    ```
- **Response:**
    - Returns all posts made by the authenticated user.
    - Caches data for up to 5 minutes to optimize performance.
    - Returns an error for invalid or missing token.
    - Uses token-based authentication.

### 5. DeletePost Endpoint
- **DELETE /delete_post/{postID}**
- **Request body:**
    ```json
    {
      "token": "user_token"
    }
    ```
- **Response:**
    - Deletes the corresponding post by `postID`.
    - Returns an error for invalid or missing token.

---

## Code Functionality and Documentation:

### Signup Endpoint

```python
@app.post("/signup")
def signup(email: str, password: str):
    """
    This endpoint registers a new user by accepting an email and password.
    
    Parameters:
    - email (str): User's email address.
    - password (str): User's password.
    
    Returns:
    - A token (JWT or random string) for the registered user.
    - 400 Bad Request if email or password is invalid.
    """


@app.post("/login")
def login(email: str, password: str):
    """
    This endpoint authenticates a user by email and password.
    
    Parameters:
    - email (str): User's email address.
    - password (str): User's password.
    
    Returns:
    - A token (JWT or random string) upon successful login.
    - 401 Unauthorized if credentials are incorrect.
    """



@app.post("/add_post")
def add_post(token: str, text: str):
    """
    Adds a new post for the authenticated user.
    
    Parameters:
    - token (str): User's authentication token.
    - text (str): The content of the post.
    
    Returns:
    - postID (str) of the newly created post.
    - 400 Bad Request if validation fails (payload exceeds 1 MB or token is invalid).
    """



@app.get("/get_posts")
def get_posts(token: str):
    """
    Retrieves all posts for the authenticated user.

    Parameters:
    - token (str): User's authentication token.

    Returns:
    - List of posts made by the user.
    - 401 Unauthorized if token is invalid or missing.
    """




@app.delete("/delete_post/{postID}")
def delete_post(postID: int, token: str):
    """
    Deletes a specific post identified by postID for the authenticated user.

    Parameters:
    - postID (int): The ID of the post to be deleted.
    - token (str): User's authentication token.

    Returns:
    - 200 OK if post is successfully deleted.
    - 401 Unauthorized if token is invalid or missing.
    """


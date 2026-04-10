# FASTAPI (SQLITE)

# FastAPI:
# Web framework for building APIs (endpoint)
# Type hints support
# Interactive API documentation (Swagger UI)
# pip install fastapi uvicorn
# 
# Pydantic:
# Data validation and parsing using Python type hints.
# IDE support with type hints
# JSON serialization/deserialization (Python to JSON to Python)
# pip install pydantic

# Hypertext Transfer Protocol(HTTP) Methods:
# @app.get() - GET requests (Read)
# @app.post() - POST requests (Create)
# @app.put() - PUT requests (Update)
# @app.delete() - DELETE requests (Delete)
# @app.patch() - PATCH requests (Partial Update)

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
import sqlite3
from sqlite import DatabaseManager

app = FastAPI(title="sqlite database API", version="1.0.0")

# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    created_at: str

class PostCreate(BaseModel):
    user_id: int
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    created_at: str

class PostResponseForUser(BaseModel):
    id: int
    title: str
    content: str
    created_at: str

# Initialize database
db = DatabaseManager()

@app.get("/")
async def root():
    return {"message": "sqlite database API", "version": "1.0.0"}

# POST - Create user
@app.post("/users/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user in the database."""
    try:
        user_id = db.create_user(user.name, user.email, user.age)
        if user_id:
            return {"id": user_id, "message": "User created successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Failed to create user")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))

# GET - Get user by ID
@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get a user by ID."""
    try:
        with sqlite3.connect(db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")

        return UserResponse(
            id=user[0],
            name=user[1],
            email=user[2],
            age=user[3],
            created_at=user[4]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occurred: {str(e)}")

# GET - Get all posts for a user
@app.get("/users/{user_id}/posts", response_model=List[PostResponseForUser])
async def get_user_posts(user_id: int):
    """Get all posts for a user."""
    try:
        with sqlite3.connect(db.db_name) as conn:
            cursor = conn.cursor()
            # Check user exists
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="User not found")

        posts = db.get_users_posts(user_id)
        return [
            PostResponseForUser(
                id=post[0],
                title=post[1],     # Fixed indices (4-column result)
                content=post[2],
                created_at=post[3]
            )
            for post in posts
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occurred: {str(e)}")

# POST - Create post
@app.post("/posts/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate):
    """Create a new post."""
    try:
        post_id = db.create_post(post.user_id, post.title, post.content)
        if post_id:
            return {"id": post_id, "message": "Post created successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Failed to create post")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))

# GET - Get post by ID
@app.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int):
    """Get a post by ID."""
    try:
        with sqlite3.connect(db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
            post = cursor.fetchone()

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Post not found")

        return PostResponse(
            id=post[0],
            user_id=post[1],
            title=post[2],
            content=post[3],
            created_at=post[4]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occurred: {str(e)}")

# DELETE - Delete user
@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    """Delete a user by ID."""
    try:
        with sqlite3.connect(db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="User not found")

        success = db.delete_user(user_id)
        if success:
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occurred: {str(e)}")

# DELETE - Delete post
@app.delete("/posts/{post_id}", response_model=dict)
async def delete_post(post_id: int):
    """Delete a specific post."""
    try:
        with sqlite3.connect(db.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Post not found")
            cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))  # Actually delete!

        return {"message": "Post deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
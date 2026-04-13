# FASTAPI (MONGO)

# Hypertext Transfer Protocol(HTTP) Methods:
# @app.get() - GET requests (Read)
# @app.post() - POST requests (Create)
# @app.put() - PUT requests (Update)
# @app.delete() - DELETE requests (Delete)
# @app.patch() - PATCH requests (Partial Update)


from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from bson.objectid import ObjectId
from datetime import datetime
from contextlib import asynccontextmanager
from mongoDB import DatabaseManager
import os
from dotenv import load_dotenv

load_dotenv()

# initialize db at module level
try:
    db = DatabaseManager()
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    db = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    if db is None:
        raise Exception("Failed to connect to MongoDB. Please check your connection settings.")
    yield
    if db:
        db.close_connection()

app = FastAPI(title="FastAPI with MongoDB", version="1.0.0", lifespan=lifespan)


# Pydantic models
class Usercreate(BaseModel):
    name: str
    email: EmailStr
    age: int

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    age: int
    created_at: datetime

class Postcreate(BaseModel):
    user_id: str
    title: str
    content: str

class PostResponse(BaseModel):
    id: str
    user_id: str
    title: str
    content: str
    created_at: datetime

class PostResponseForUser(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with MongoDB!"}


@app.get("/users/", response_model=List[UserResponse])
async def get_all_users():
    """Get all users"""
    try:
        users = db.get_all_users()
        return [UserResponse(
            id=str(user['_id']),
            name=user['name'],
            email=user['email'],
            age=user['age'],
            created_at=user['created_at']
        ) for user in users]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    """Get a user by ID"""
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")

        user = db.users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return UserResponse(
            id=str(user['_id']), 
            name=user['name'],
            email=user['email'],
            age=user['age'],
            created_at=user['created_at']
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: Usercreate):
    """Create a new user"""
    try:
        user_id = db.create_user(user.name, user.email, user.age)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create user")

        created = db.users_collection.find_one({"_id": ObjectId(user_id)})
        return UserResponse(
            id=str(created['_id']),
            name=created['name'],
            email=created['email'],
            age=created['age'],
            created_at=created['created_at']
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/posts/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_post(post: Postcreate):
    """Create a new post"""
    try:
        if not ObjectId.is_valid(post.user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")

        user = db.users_collection.find_one({"_id": ObjectId(post.user_id)})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        post_id = db.create_post(post.user_id, post.title, post.content)
        if post_id:
            return {"message": "Post created successfully", "id": post_id}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create post")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/users/{user_id}/posts", response_model=List[PostResponseForUser])
async def get_user_posts(user_id: str):
    """Get all posts for a user"""
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")

        user = db.users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        posts = db.get_posts_by_user_id(user_id)
        return [PostResponseForUser(
            id=str(post['_id']),
            title=post['title'],
            content=post['content'],
            created_at=post['created_at']
        ) for post in posts]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/posts/", response_model=List[PostResponse])
async def get_all_posts():
    """Get all posts"""
    try:
        posts = list(db.posts_collection.find().sort("created_at", -1))
        return [PostResponse(
            id=str(post['_id']),
            user_id=str(post['user_id']),
            title=post['title'],
            content=post['content'],
            created_at=post['created_at']
        ) for post in posts]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.delete("/posts/{post_id}", response_model=dict)
async def delete_post(post_id: str):
    """Delete a post by ID"""
    try:
        if not ObjectId.is_valid(post_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid post ID format")

        result = db.posts_collection.delete_one({"_id": ObjectId(post_id)})
        if result.deleted_count == 1:
            return {"message": "Post deleted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.put("/users/{user_id}", response_model=dict)
async def update_user(user_id: str, user: Usercreate):
    """Update a user's information"""
    try:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")

        existing_user = db.users_collection.find_one({"_id": ObjectId(user_id)})
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        result = db.users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"name": user.name, "email": user.email, "age": user.age}}
        )
        if result.modified_count > 0:
            return {"message": "User updated successfully"}
        else:
            return {"message": "No changes made to the user"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.put("/posts/{post_id}", response_model=dict)
async def update_post(post_id: str, title: str, content: str):
    """Update a post's title and content"""
    try:
        if not ObjectId.is_valid(post_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid post ID format")

        existing_post = db.posts_collection.find_one({"_id": ObjectId(post_id)})
        if not existing_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        result = db.posts_collection.update_one(
            {"_id": ObjectId(post_id)},
            {"$set": {"title": title, "content": content}}
        )
        if result.modified_count > 0:
            return {"message": "Post updated successfully"}
        else:
            return {"message": "No changes made to the post"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")
    
@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: str, confirm: bool = False):
    """Delete a user and their posts"""
    try:
        if not confirm:
            return {"message": "Please pass confirm=true to delete the user"}

        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")

        existing_user = db.users_collection.find_one({"_id": ObjectId(user_id)})
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        result = db.delete_user(user_id)
        if result:
            return {"message": "User and their posts deleted successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete user")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
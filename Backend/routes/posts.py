from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
import uuid
import shutil
from pathlib import Path

from models import PostDB, UserDB, CommentDB
from schemas import Post, PostCreate, Comment, CommentBase, Category
from dependencies import get_db, get_current_active_user, convert_to_db_types

post_router = APIRouter(prefix="/posts", tags=["Posts"])

# Configure CORS
origins = [
    "http://localhost:3000",  # React default
    "http://localhost:5173",  # Vite default
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    # Add your frontend URL here
]

# Note: This middleware should be added to the main app, not here.
# This is just a reference for the main.py file.

# Create directory for post images if it doesn't exist
UPLOAD_DIR = Path("static/uploads/posts")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Helper function to convert PostDB objects to the Pydantic schema
def convert_post_db_to_schema(post_db: PostDB) -> Post:
    # Extract the user IDs from the likes relationship
    like_ids = [user.id for user in post_db.likes] if post_db.likes else []
    
    # Информация об авторе поста
    author_data = {
        "id": post_db.author_id,
        "username": post_db.author.username if post_db.author else "Неизвестный пользователь"
    }
    
    # Create a Post object with the right format for likes
    post_dict = {
        "id": post_db.id,
        "title": post_db.title,
        "content": post_db.content,
        "author_id": post_db.author_id,
        "author": author_data,  # Добавляем информацию об авторе
        "photo_url": post_db.photo_url,
        "category": post_db.category,
        "created_at": post_db.created_at,
        "updated_at": post_db.updated_at,
        "likes": like_ids,
        "comments": post_db.comments
    }
    
    return Post.parse_obj(post_dict)

@post_router.get("", response_model=List[Post])
async def read_posts(skip: int = 0, limit: int = 100, category: Optional[Category] = None, db: Session = Depends(get_db)):
    if category:
        posts = db.query(PostDB).filter(PostDB.category == category).offset(skip).limit(limit).all()
    else:
        posts = db.query(PostDB).offset(skip).limit(limit).all()
    
    # Convert PostDB objects to the Pydantic schema
    return [convert_post_db_to_schema(post) for post in posts]

@post_router.get("/{post_id}", response_model=Post)
async def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return convert_post_db_to_schema(post)

@post_router.post("", response_model=Post)
async def create_post(post: PostCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    post_dict = convert_to_db_types(post)
    
    db_post = PostDB(**post_dict, author_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return convert_post_db_to_schema(db_post)

@post_router.post("/upload", response_model=Post)
async def create_post_with_file(
    title: str = Form(...),
    content: str = Form(...),
    category: Category = Form(Category.FLOOD),
    file: UploadFile = File(...),
    current_user: UserDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Validate image type
    content_type = file.content_type
    if not content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Create unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_location = UPLOAD_DIR / unique_filename
    
    # Save file
    try:
        with file_location.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
    
    # Create absolute URL for the image
    base_url = "http://localhost:8000"  # Replace with your base URL in production
    photo_url = f"{base_url}/static/uploads/posts/{unique_filename}"
    
    # Create post
    try:
        db_post = PostDB(
            title=title,
            content=content,
            author_id=current_user.id,
            photo_url=photo_url,
            category=category
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return convert_post_db_to_schema(db_post)
    except Exception as e:
        # Remove uploaded file in case of error
        if file_location.exists():
            os.remove(file_location)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating post: {str(e)}"
        )

@post_router.put("/{post_id}", response_model=Post)
async def update_post(post_id: int, post: PostCreate, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    post_dict = convert_to_db_types(post)
    
    for key, value in post_dict.items():
        setattr(db_post, key, value)
    
    db_post.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_post)
    return convert_post_db_to_schema(db_post)

@post_router.put("/{post_id}/upload", response_model=Post)
async def update_post_with_file(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    category: Category = Form(Category.FLOOD),
    file: Optional[UploadFile] = File(None),
    current_user: UserDB = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Check if post exists
    db_post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check permissions
    if db_post.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Update basic fields
    db_post.title = title
    db_post.content = content
    db_post.category = category
    db_post.updated_at = datetime.utcnow()
    
    # Handle file upload if provided
    if file:
        # Validate image type
        content_type = file.content_type
        if not content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image"
            )
        
        # Create unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_location = UPLOAD_DIR / unique_filename
        
        # Save file
        try:
            with file_location.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
                
            # Delete old image if exists
            if db_post.photo_url:
                old_filename = db_post.photo_url.split("/")[-1]
                old_file_path = UPLOAD_DIR / old_filename
                if old_file_path.exists():
                    os.remove(old_file_path)
            
            # Update photo URL
            base_url = "http://localhost:8000"  # Replace with your base URL in production
            db_post.photo_url = f"{base_url}/static/uploads/posts/{unique_filename}"
        finally:
            file.file.close()
    
    # Save changes
    db.commit()
    db.refresh(db_post)
    return convert_post_db_to_schema(db_post)

@post_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.author_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Delete associated image if exists
    if db_post.photo_url:
        try:
            filename = db_post.photo_url.split("/")[-1]
            file_path = UPLOAD_DIR / filename
            if file_path.exists():
                os.remove(file_path)
        except Exception:
            # Continue with post deletion even if image deletion fails
            pass
    
    db.delete(db_post)
    db.commit()
    return None

@post_router.post("/{post_id}/like", response_model=Post)
async def like_post(post_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if current_user in db_post.likes:
        raise HTTPException(status_code=400, detail="User already liked this post")
    
    db_post.likes.append(current_user)
    db.commit()
    db.refresh(db_post)
    return convert_post_db_to_schema(db_post)

@post_router.post("/{post_id}/unlike", response_model=Post)
async def unlike_post(post_id: int, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if current_user not in db_post.likes:
        raise HTTPException(status_code=400, detail="User has not liked this post")
    
    db_post.likes.remove(current_user)
    db.commit()
    db.refresh(db_post)
    return convert_post_db_to_schema(db_post)

@post_router.post("/{post_id}/comments", response_model=Comment)
async def create_comment(post_id: int, comment: CommentBase, current_user: UserDB = Depends(get_current_active_user), db: Session = Depends(get_db)):
    db_post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comment_dict = convert_to_db_types(comment)
    
    db_comment = CommentDB(**comment_dict, post_id=post_id, author_id=current_user.id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment 
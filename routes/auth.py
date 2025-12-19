from fastapi import APIRouter, HTTPException, status, Response
from datetime import datetime, timedelta
from bson import ObjectId

from models.user import UserCreate, UserLogin, UserResponse
from utils.database import get_database
from utils.security import get_password_hash, verify_password, create_access_token
from utils.helpers import serialize_doc

router = APIRouter()

@router.post("/signup", response_model=dict)
async def signup(user: UserCreate):
    """Register a new user"""
    db = get_database()
    
    # Check if username exists
    existing_user = await db.users.find_one({"username": user.username.lower()})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    existing_email = await db.users.find_one({"email": user.email})
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user document
    user_doc = {
        "username": user.username.lower(),
        "email": user.email,
        "pin_hash": get_password_hash(user.pin),
        "full_name": user.full_name,
        "created_at": datetime.utcnow(),
        "total_owed": 0.0,
        "total_owing": 0.0
    }
    
    result = await db.users.insert_one(user_doc)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.username.lower(), "user_id": str(result.inserted_id)}
    )
    
    return {
        "message": "User created successfully",
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username.lower()
    }

@router.post("/login", response_model=dict)
async def login(user: UserLogin, response: Response):
    """Login user"""
    db = get_database()
    
    # Find user
    user_doc = await db.users.find_one({"username": user.username.lower()})
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or PIN"
        )
    
    # Verify PIN
    if not verify_password(user.pin, user_doc["pin_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or PIN"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.username.lower(), "user_id": str(user_doc["_id"])}
    )
    
    # Set cookie
    response.set_cookie(
        key="token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )
    
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username.lower()
    }

@router.post("/logout")
async def logout(response: Response):
    """Logout user"""
    response.delete_cookie(key="token")
    return {"message": "Logged out successfully"}

ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 days

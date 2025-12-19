from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from models.user import UserResponse, UserUpdate
from models.notification import NotificationResponse
from utils.database import get_database
from utils.security import get_current_user
from utils.helpers import serialize_doc

router = APIRouter()

@router.get("/me", response_model=dict)
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """Get current user profile"""
    db = get_database()
    
    user = await db.users.find_one({"username": current_user["username"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return serialize_doc(user)

@router.get("/search/{username}", response_model=dict)
async def search_user(username: str, current_user: dict = Depends(get_current_user)):
    """Search for a user by username"""
    db = get_database()
    
    user = await db.users.find_one({"username": username.lower()})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "username": user["username"],
        "full_name": user.get("full_name"),
        "exists": True
    }

@router.get("/notifications", response_model=dict)
async def get_notifications(current_user: dict = Depends(get_current_user)):
    """Get user notifications"""
    db = get_database()
    
    notifications = await db.notifications.find({
        "user_username": current_user["username"]
    }).sort("created_at", -1).limit(50).to_list(50)
    
    unread_count = await db.notifications.count_documents({
        "user_username": current_user["username"],
        "read": False
    })
    
    return {
        "notifications": serialize_doc(notifications),
        "unread_count": unread_count
    }

@router.post("/notifications/{notification_id}/read", response_model=dict)
async def mark_notification_read(notification_id: str, current_user: dict = Depends(get_current_user)):
    """Mark notification as read"""
    db = get_database()
    
    from bson import ObjectId
    try:
        result = await db.notifications.update_one(
            {"_id": ObjectId(notification_id), "user_username": current_user["username"]},
            {"$set": {"read": True}}
        )
    except:
        raise HTTPException(status_code=400, detail="Invalid notification ID")
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return {"message": "Notification marked as read"}

@router.get("/stats", response_model=dict)
async def get_user_stats(current_user: dict = Depends(get_current_user)):
    """Get user statistics"""
    db = get_database()
    
    from models.debt import DebtStatus
    
    # Count debts
    total_debts_created = await db.debts.count_documents({"creditor_username": current_user["username"]})
    total_debts_received = await db.debts.count_documents({"debtor_username": current_user["username"]})
    active_debts = await db.debts.count_documents({
        "$or": [
            {"creditor_username": current_user["username"]},
            {"debtor_username": current_user["username"]}
        ],
        "status": DebtStatus.ACTIVE
    })
    paid_debts = await db.debts.count_documents({
        "$or": [
            {"creditor_username": current_user["username"]},
            {"debtor_username": current_user["username"]}
        ],
        "status": DebtStatus.PAID
    })
    
    # Get user totals
    user = await db.users.find_one({"username": current_user["username"]})
    
    return {
        "total_debts_created": total_debts_created,
        "total_debts_received": total_debts_received,
        "active_debts": active_debts,
        "paid_debts": paid_debts,
        "total_owed_to_me": user.get("total_owed", 0.0),
        "total_i_owe": user.get("total_owing", 0.0),
        "net_balance": user.get("total_owed", 0.0) - user.get("total_owing", 0.0)
    }

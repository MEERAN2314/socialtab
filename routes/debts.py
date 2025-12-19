from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from bson import ObjectId
from typing import List

from models.debt import DebtCreate, DebtResponse, DebtAction, DebtStatus, DebtType
from models.notification import NotificationCreate, NotificationType
from utils.database import get_database
from utils.security import get_current_user
from utils.helpers import serialize_doc, calculate_group_split

router = APIRouter()

@router.post("/create", response_model=dict)
async def create_debt(debt: DebtCreate, current_user: dict = Depends(get_current_user)):
    """Create a new debt"""
    db = get_database()
    
    # Verify debtor exists
    debtor = await db.users.find_one({"username": debt.debtor_username.lower()})
    if not debtor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Debtor user not found"
        )
    
    # Can't create debt to yourself
    if debt.debtor_username.lower() == current_user["username"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create debt to yourself"
        )
    
    # Create debt document
    debt_doc = {
        "creditor_username": current_user["username"],
        "creditor_id": ObjectId(current_user["user_id"]),
        "debtor_username": debt.debtor_username.lower(),
        "debtor_id": debtor["_id"],
        "amount": debt.amount,
        "description": debt.description,
        "status": DebtStatus.PENDING,
        "debt_type": debt.debt_type,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "paid_at": None
    }
    
    # Handle group debts
    if debt.debt_type == DebtType.GROUP and debt.participants:
        participants = calculate_group_split(debt.amount, [p.dict() for p in debt.participants])
        debt_doc["participants"] = participants
    
    result = await db.debts.insert_one(debt_doc)
    
    # Create notification for debtor
    notification = {
        "user_username": debt.debtor_username.lower(),
        "notification_type": NotificationType.DEBT_REQUEST,
        "title": "New Debt Request",
        "message": f"{current_user['username']} says you owe ${debt.amount:.2f} for {debt.description}",
        "debt_id": str(result.inserted_id),
        "action_url": f"/debts/{result.inserted_id}",
        "read": False,
        "created_at": datetime.utcnow()
    }
    await db.notifications.insert_one(notification)
    
    return {
        "message": "Debt created successfully",
        "debt_id": str(result.inserted_id),
        "status": "pending_acceptance"
    }

@router.get("/my-debts", response_model=dict)
async def get_my_debts(current_user: dict = Depends(get_current_user)):
    """Get all debts for current user"""
    db = get_database()
    
    # Debts where user is creditor (people owe them)
    owed_to_me = await db.debts.find({
        "creditor_username": current_user["username"],
        "status": {"$in": [DebtStatus.PENDING, DebtStatus.ACTIVE]}
    }).to_list(100)
    
    # Debts where user is debtor (they owe others)
    i_owe = await db.debts.find({
        "debtor_username": current_user["username"],
        "status": {"$in": [DebtStatus.PENDING, DebtStatus.ACTIVE]}
    }).to_list(100)
    
    return {
        "owed_to_me": serialize_doc(owed_to_me),
        "i_owe": serialize_doc(i_owe),
        "total_owed_to_me": sum(d["amount"] for d in owed_to_me if d["status"] == DebtStatus.ACTIVE),
        "total_i_owe": sum(d["amount"] for d in i_owe if d["status"] == DebtStatus.ACTIVE)
    }

@router.get("/history", response_model=dict)
async def get_debt_history(current_user: dict = Depends(get_current_user)):
    """Get debt history (paid/archived)"""
    db = get_database()
    
    history = await db.debts.find({
        "$or": [
            {"creditor_username": current_user["username"]},
            {"debtor_username": current_user["username"]}
        ],
        "status": {"$in": [DebtStatus.PAID, DebtStatus.ARCHIVED]}
    }).sort("updated_at", -1).to_list(50)
    
    return {
        "history": serialize_doc(history)
    }

@router.get("/{debt_id}", response_model=dict)
async def get_debt_detail(debt_id: str, current_user: dict = Depends(get_current_user)):
    """Get debt details"""
    db = get_database()
    
    try:
        debt = await db.debts.find_one({"_id": ObjectId(debt_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid debt ID")
    
    if not debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    
    # Check if user is involved in this debt
    if debt["creditor_username"] != current_user["username"] and debt["debtor_username"] != current_user["username"]:
        raise HTTPException(status_code=403, detail="Not authorized to view this debt")
    
    return serialize_doc(debt)

@router.post("/{debt_id}/action", response_model=dict)
async def debt_action(debt_id: str, action: DebtAction, current_user: dict = Depends(get_current_user)):
    """Perform action on debt (accept, dispute, mark_paid, confirm_paid)"""
    db = get_database()
    
    try:
        debt = await db.debts.find_one({"_id": ObjectId(debt_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid debt ID")
    
    if not debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    
    update_data = {"updated_at": datetime.utcnow()}
    notification_data = None
    
    if action.action == "accept":
        # Debtor accepts the debt
        if debt["debtor_username"] != current_user["username"]:
            raise HTTPException(status_code=403, detail="Only debtor can accept")
        if debt["status"] != DebtStatus.PENDING:
            raise HTTPException(status_code=400, detail="Debt is not pending")
        
        update_data["status"] = DebtStatus.ACTIVE
        notification_data = {
            "user_username": debt["creditor_username"],
            "notification_type": NotificationType.DEBT_ACCEPTED,
            "title": "Debt Accepted",
            "message": f"{current_user['username']} accepted the debt of ${debt['amount']:.2f}",
            "debt_id": debt_id,
            "read": False,
            "created_at": datetime.utcnow()
        }
        
        # Update user totals
        await db.users.update_one(
            {"username": debt["creditor_username"]},
            {"$inc": {"total_owed": debt["amount"]}}
        )
        await db.users.update_one(
            {"username": debt["debtor_username"]},
            {"$inc": {"total_owing": debt["amount"]}}
        )
    
    elif action.action == "dispute":
        # Debtor disputes the debt
        if debt["debtor_username"] != current_user["username"]:
            raise HTTPException(status_code=403, detail="Only debtor can dispute")
        
        update_data["status"] = DebtStatus.DISPUTED
        update_data["dispute_reason"] = action.reason
        notification_data = {
            "user_username": debt["creditor_username"],
            "notification_type": NotificationType.DEBT_DISPUTED,
            "title": "Debt Disputed",
            "message": f"{current_user['username']} disputed the debt. Reason: {action.reason}",
            "debt_id": debt_id,
            "read": False,
            "created_at": datetime.utcnow()
        }
    
    elif action.action == "mark_paid":
        # Debtor marks as paid
        if debt["debtor_username"] != current_user["username"]:
            raise HTTPException(status_code=403, detail="Only debtor can mark as paid")
        if debt["status"] != DebtStatus.ACTIVE:
            raise HTTPException(status_code=400, detail="Debt is not active")
        
        update_data["status"] = DebtStatus.PAID
        update_data["paid_at"] = datetime.utcnow()
        notification_data = {
            "user_username": debt["creditor_username"],
            "notification_type": NotificationType.PAYMENT_CONFIRMED,
            "title": "Payment Made",
            "message": f"{current_user['username']} marked ${debt['amount']:.2f} as paid",
            "debt_id": debt_id,
            "read": False,
            "created_at": datetime.utcnow()
        }
        
        # Update user totals
        await db.users.update_one(
            {"username": debt["creditor_username"]},
            {"$inc": {"total_owed": -debt["amount"]}}
        )
        await db.users.update_one(
            {"username": debt["debtor_username"]},
            {"$inc": {"total_owing": -debt["amount"]}}
        )
    
    # Update debt
    await db.debts.update_one({"_id": ObjectId(debt_id)}, {"$set": update_data})
    
    # Create notification
    if notification_data:
        await db.notifications.insert_one(notification_data)
    
    return {"message": f"Debt {action.action} successful", "status": update_data.get("status", debt["status"])}

@router.delete("/{debt_id}", response_model=dict)
async def delete_debt(debt_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a pending debt (only creditor can delete)"""
    db = get_database()
    
    try:
        debt = await db.debts.find_one({"_id": ObjectId(debt_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid debt ID")
    
    if not debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    
    if debt["creditor_username"] != current_user["username"]:
        raise HTTPException(status_code=403, detail="Only creditor can delete")
    
    if debt["status"] != DebtStatus.PENDING:
        raise HTTPException(status_code=400, detail="Can only delete pending debts")
    
    await db.debts.delete_one({"_id": ObjectId(debt_id)})
    
    return {"message": "Debt deleted successfully"}

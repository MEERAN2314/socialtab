from datetime import datetime, timedelta
from typing import List, Dict
from bson import ObjectId

def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable format"""
    if doc is None:
        return None
    
    if isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    
    if isinstance(doc, dict):
        serialized = {}
        for key, value in doc.items():
            if key == "_id":
                serialized["id"] = str(value)
            elif isinstance(value, ObjectId):
                serialized[key] = str(value)
            elif isinstance(value, datetime):
                serialized[key] = value.isoformat()
            elif isinstance(value, dict):
                serialized[key] = serialize_doc(value)
            elif isinstance(value, list):
                serialized[key] = [serialize_doc(item) for item in value]
            else:
                serialized[key] = value
        return serialized
    
    return doc

def calculate_group_split(total_amount: float, participants: List[Dict]) -> List[Dict]:
    """Calculate how much each person owes in a group split"""
    split_type = participants[0].get("split_type", "equal")
    
    if split_type == "equal":
        per_person = total_amount / len(participants)
        for participant in participants:
            participant["amount"] = round(per_person, 2)
    else:
        # Custom split - amounts already provided
        pass
    
    return participants

def is_debt_expired(created_at: datetime, days: int = 90) -> bool:
    """Check if debt is older than specified days (Dead Man's Switch)"""
    expiry_date = created_at + timedelta(days=days)
    return datetime.utcnow() > expiry_date

def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"${amount:.2f}"

def validate_pin(pin: str) -> bool:
    """Validate PIN format (4-6 digits)"""
    return pin.isdigit() and 4 <= len(pin) <= 6

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    DEBT_REQUEST = "debt_request"
    DEBT_ACCEPTED = "debt_accepted"
    DEBT_DISPUTED = "debt_disputed"
    PAYMENT_REQUEST = "payment_request"
    PAYMENT_CONFIRMED = "payment_confirmed"
    REMINDER = "reminder"

class NotificationCreate(BaseModel):
    user_username: str
    notification_type: NotificationType
    title: str
    message: str
    debt_id: Optional[str] = None
    action_url: Optional[str] = None

class NotificationResponse(BaseModel):
    id: str
    user_username: str
    notification_type: NotificationType
    title: str
    message: str
    debt_id: Optional[str] = None
    action_url: Optional[str] = None
    read: bool = False
    created_at: datetime

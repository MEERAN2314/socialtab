from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class DebtStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    DISPUTED = "disputed"
    PAID = "paid"
    ARCHIVED = "archived"

class DebtType(str, Enum):
    SINGLE = "single"
    GROUP = "group"

class Participant(BaseModel):
    username: str
    amount: float
    accepted: bool = False

class DebtCreate(BaseModel):
    amount: float = Field(..., gt=0)
    description: str = Field(..., min_length=1, max_length=200)
    debtor_username: str
    debt_type: DebtType = DebtType.SINGLE
    participants: Optional[List[Participant]] = None
    
    @validator('amount')
    def amount_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return round(v, 2)

class DebtResponse(BaseModel):
    id: str
    creditor_username: str
    debtor_username: str
    amount: float
    description: str
    status: DebtStatus
    debt_type: DebtType
    participants: Optional[List[Participant]] = None
    created_at: datetime
    updated_at: datetime
    paid_at: Optional[datetime] = None

class DebtUpdate(BaseModel):
    status: Optional[DebtStatus] = None
    description: Optional[str] = None

class DebtAction(BaseModel):
    action: str  # accept, dispute, mark_paid, confirm_paid
    reason: Optional[str] = None

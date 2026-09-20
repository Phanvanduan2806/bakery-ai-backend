from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ConversationCreate(BaseModel):
    title: Optional[str] = None


class ConversationUpdate(BaseModel):
    title: str


class ConversationResponse(BaseModel):
    id: int
    user_id: int
    title: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

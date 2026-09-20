from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Conversation, Message

from app.schemas.conversation import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
)

from app.schemas.message import (
    MessageCreate,
    MessageResponse,
)

from app.services.kho import get_current_user


router = APIRouter(
    prefix="/ai/conversations",
    tags=["AI Conversations"],
)


security = HTTPBearer()


# =========================================================
# GET USER ID
# =========================================================

def get_user_id(
    credentials: HTTPAuthorizationCredentials,
) -> int:

    authorization = (
        f"Bearer {credentials.credentials}"
    )

    user = get_current_user(
        authorization
    )

    user_id = user.get("id")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Không xác định được user",
        )

    return int(user_id)


# =========================================================
# CREATE CONVERSATION
# =========================================================

@router.post(
    "",
    response_model=ConversationResponse,
)
def create_conversation(
    data: ConversationCreate,
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db),
):

    user_id = get_user_id(
        credentials
    )

    conversation = Conversation(
        user_id=user_id,
        title=data.title,
    )

    db.add(conversation)

    db.commit()

    db.refresh(conversation)

    return conversation


# =========================================================
# GET CONVERSATIONS
# =========================================================

@router.get(
    "",
    response_model=list[ConversationResponse],
)
def get_conversations(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db),
):

    user_id = get_user_id(
        credentials
    )

    conversations = (
        db.query(Conversation)
        .filter(
            Conversation.user_id == user_id
        )
        .order_by(
            Conversation.updated_at.desc()
        )
        .all()
    )

    return conversations


# =========================================================
# UPDATE CONVERSATION TITLE
# =========================================================

@router.patch(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def update_conversation(
    conversation_id: int,
    data: ConversationUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db),
):

    user_id = get_user_id(
        credentials
    )

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation không tồn tại",
        )

    conversation.title = data.title.strip()

    conversation.updated_at = datetime.utcnow()

    db.commit()

    db.refresh(conversation)

    return conversation


# =========================================================
# CREATE MESSAGE
# =========================================================

@router.post(
    "/{conversation_id}/messages",
    response_model=MessageResponse,
)
def create_message(
    conversation_id: int,
    data: MessageCreate,
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db),
):

    user_id = get_user_id(
        credentials
    )

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation không tồn tại",
        )

    message = Message(
        conversation_id=conversation_id,
        role=data.role,
        content=data.content,
    )

    db.add(message)

    conversation.updated_at = datetime.utcnow()

    db.commit()

    db.refresh(message)

    return message


# =========================================================
# GET MESSAGES
# =========================================================

@router.get(
    "/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
def get_messages(
    conversation_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db),
):

    user_id = get_user_id(
        credentials
    )

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation không tồn tại",
        )

    messages = (
        db.query(Message)
        .filter(
            Message.conversation_id
            == conversation_id
        )
        .order_by(
            Message.created_at.asc()
        )
        .all()
    )

    return messages

# =========================================================
# DELETE CONVERSATION
# =========================================================

@router.delete(
    "/{conversation_id}"
)
def delete_conversation(
    conversation_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db),
):
    user_id = get_user_id(credentials)

    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        .first()
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation không tồn tại",
        )

    db.delete(conversation)
    db.commit()

    return {
        "success": True,
        "message": "Đã xoá cuộc trò chuyện",
    }
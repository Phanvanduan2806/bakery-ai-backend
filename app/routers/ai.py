from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Conversation, Message

from app.schemas.ai import ChatRequest, ChatResponse

from app.services.ai.chat import chat_with_ai
from app.services.kho.ingredients import get_ingredients
from app.services.kho.stock import get_stock
from app.services.kho.exports_single import get_single_exports
from app.services.kho.exports_recipe import get_recipe_exports
from app.services.kho import get_current_user
from app.services.kho.recipes import get_recipes
from app.services.kho.imports import get_imports

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


security = HTTPBearer()

# =========================================================
# CHAT
# =========================================================

@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    try:
        # =================================================
        # 1. LẤY USER HIỆN TẠI
        # =================================================

        authorization = f"Bearer {credentials.credentials}"

        user = get_current_user(
            authorization
        )

        user_id = user.get("id")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Không xác định được user"
            )

        # =================================================
        # 2. KIỂM TRA CONVERSATION
        # =================================================

        conversation = (
            db.query(Conversation)
            .filter(
                Conversation.id == request.conversation_id,
                Conversation.user_id == user_id,
            )
            .first()
        )

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation không tồn tại"
            )

        # =================================================
        # 3. GỌI AI
        # =================================================

        answer = chat_with_ai(
            message=request.message,
            authorization=authorization,
            db=db,
            conversation_id=request.conversation_id,
        )

        # =================================================
        # 4. LƯU MESSAGE CỦA USER
        # =================================================

        user_message = Message(
            conversation_id=request.conversation_id,
            role="user",
            content=request.message,
        )

        db.add(user_message)

        # =================================================
        # 5. LƯU MESSAGE CỦA ASSISTANT
        # =================================================

        assistant_message = Message(
            conversation_id=request.conversation_id,
            role="assistant",
            content=answer,
        )

        db.add(assistant_message)

        # =================================================
        # 6. CẬP NHẬT CONVERSATION
        # =================================================

        conversation.updated_at = datetime.utcnow()

        db.commit()

        # =================================================
        # 7. TRẢ RESPONSE
        # =================================================

        return ChatResponse(
            message=answer
        )

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        error_message = str(e)

        print(
            "❌ AI CHAT ERROR:",
            error_message
        )

        # =================================================
        # GEMINI / AI QUOTA
        # =================================================

        if (
            "429" in error_message
            or "RESOURCE_EXHAUSTED" in error_message
        ):
            raise HTTPException(
                status_code=429,
                detail=(
                    "AI hiện đang tạm thời hết lượt sử dụng. "
                    "Vui lòng thử lại sau."
                )
            )

        # =================================================
        # LỖI KHÁC
        # =================================================

        raise HTTPException(
            status_code=500,
            detail=(
                "AI hiện đang tạm thời không khả dụng. "
                "Vui lòng thử lại sau."
            )
        )
# =========================================================
# INGREDIENTS
# =========================================================

@router.get("/ingredients")
def ingredients(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:

        data = get_ingredients(
            f"Bearer {credentials.credentials}"
        )

        return {
            "success": True,
            "data": data
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# STOCK
# =========================================================

@router.get("/stock")
def stock(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:

        data = get_stock(
            f"Bearer {credentials.credentials}"
        )

        return {
            "success": True,
            "data": data
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================================================
# XUẤT LẺ - LỊCH SỬ
# =========================================================

@router.get("/exports/single")
def export_single(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:

        data = get_single_exports(
            f"Bearer {credentials.credentials}"
        )

        return {
            "success": True,
            "data": data
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
# =========================================================
# XUẤT Công thức - LỊCH SỬ
# =========================================================

@router.get("/exports/recipe")
def export_single(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:

        data = get_recipe_exports(
            f"Bearer {credentials.credentials}"
        )

        return {
            "success": True,
            "data": data
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =========================================================
# RECIPES
# =========================================================

@router.get("/recipes")
def recipes(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:

        authorization = (
            f"Bearer {credentials.credentials}"
        )

        data = get_recipes(
            authorization
        )

        return {
            "success": True,
            "data": data
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
        
# =========================================================
# Nhập kho
# =========================================================

@router.get("/imports")
def recipes(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:

        authorization = (
            f"Bearer {credentials.credentials}"
        )

        data = get_imports(
            authorization
        )

        return {
            "success": True,
            "data": data
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =========================================================
# CURRENT USER
# =========================================================

@router.get("/me")
def me(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    authorization = f"Bearer {credentials.credentials}"

    return get_current_user(
        authorization
    )


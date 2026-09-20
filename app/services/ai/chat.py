from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Message
from app.services.ai.prompts import SYSTEM_INSTRUCTION
from app.services.ai.tools import (
    create_ingredients_tool,
    create_stock_tool,
    create_exports_single_tool,
    create_exports_recipe_tool,
    create_exports_summary_tool,
    create_recipes_tool,
    create_imports_tool
)
from app.services.ai.provider_manager import AIProviderManager


def chat_with_ai(
    message: str,
    authorization: str,
    db: Session,
    conversation_id: int,
):
    # =====================================================
    # NGÀY HIỆN TẠI
    # =====================================================

    current_date = datetime.now().strftime("%Y-%m-%d")

    system_instruction = f"""
{SYSTEM_INSTRUCTION}

==================================================
NGÀY HIỆN TẠI
==================================================

Ngày hiện tại: {current_date}

Khi người dùng chỉ cung cấp ngày và tháng
mà không có năm, hãy sử dụng năm của ngày hiện tại.

Khi người dùng đã cung cấp đầy đủ ngày, tháng, năm,
phải giữ nguyên chính xác năm người dùng đã cung cấp.

Khi gọi tool, ngày phải có định dạng YYYY-MM-DD.
"""

    # =====================================================
    # LẤY LỊCH SỬ CONVERSATION
    # =====================================================

    history = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(
            Message.created_at.asc()
        )
        .all()
    )

    messages = [
        {
            "role": item.role,
            "content": item.content,
        }
        for item in history
        if item.role in ["user", "assistant"]
    ]

    # =====================================================
    # THÊM MESSAGE HIỆN TẠI
    # =====================================================

    messages.append(
        {
            "role": "user",
            "content": message,
        }
    )

    # =====================================================
    # TOOLS
    # =====================================================

    tools = {
        "get_ingredients_tool": create_ingredients_tool(
            authorization
        ),
        "get_stock_tool": create_stock_tool(
            authorization
        ),
        "get_exports_single_tool": create_exports_single_tool(
            authorization
        ),
        "get_exports_recipe_tool": create_exports_recipe_tool(
            authorization
        ),
        "get_exports_summary_tool": create_exports_summary_tool(
            authorization
        ),
        "get_recipes_tool": create_recipes_tool(
            authorization
        ),
         "get_imports_tool": create_imports_tool(
            authorization
        ),
        
    }

    # =====================================================
    # AI PROVIDER
    # =====================================================

    manager = AIProviderManager(
        system_instruction=system_instruction,
        tools=tools,
    )

    return manager.chat(
        messages=messages
    )
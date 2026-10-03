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
    create_imports_tool,
)

from app.services.ai.provider_manager import (
    AIProviderManager,
)

from app.services.ai.dispatcher import (
    dispatch_question,
)


def select_tools_for_route(
    route: str,
    message: str,
    authorization: str,
):
    """
    Chọn tool cần thiết cho câu hỏi.

    Mục tiêu:
    - giảm token
    - giảm số tool model phải cân nhắc
    - tăng độ ổn định của Tool Calling
    """

    message_lower = message.lower()

    # =====================================================
    # TỒN KHO
    # =====================================================

    stock_keywords = [
        "tồn kho",
        "tồn",
        "còn bao nhiêu",
        "còn lại",
        "sắp hết",
        "gần hết",
        "hết hàng",
        "hết",
    ]

    if any(
        keyword in message_lower
        for keyword in stock_keywords
    ):
        return {
            "get_stock_tool":
                create_stock_tool(
                    authorization
                )
        }

    # =====================================================
    # NGUYÊN LIỆU
    # =====================================================

    ingredient_keywords = [
        "nguyên liệu",
        "giá nguyên liệu",
        "danh sách nguyên liệu",
    ]

    if any(
        keyword in message_lower
        for keyword in ingredient_keywords
    ):
        return {
            "get_ingredients_tool":
                create_ingredients_tool(
                    authorization
                )
        }

    # =====================================================
    # NHẬP KHO
    # =====================================================

    import_keywords = [
        "nhập kho",
        "nhập nguyên liệu",
        "đã nhập",
        "nhập bao nhiêu",
    ]

    if any(
        keyword in message_lower
        for keyword in import_keywords
    ):
        return {
            "get_imports_tool":
                create_imports_tool(
                    authorization
                )
        }

    # =====================================================
    # XUẤT KHO LẺ
    # =====================================================

    export_single_keywords = [
        "xuất kho",
        "xuất nguyên liệu",
        "xuất lẻ",
    ]

    if any(
        keyword in message_lower
        for keyword in export_single_keywords
    ):
        return {
            "get_exports_single_tool":
                create_exports_single_tool(
                    authorization
                )
        }

    # =====================================================
    # XUẤT THEO CÔNG THỨC
    # =====================================================

    recipe_export_keywords = [
        "xuất theo công thức",
        "xuất công thức",
    ]

    if any(
        keyword in message_lower
        for keyword in recipe_export_keywords
    ):
        return {
            "get_exports_recipe_tool":
                create_exports_recipe_tool(
                    authorization
                )
        }

    # =====================================================
    # TỔNG GIÁ TRỊ XUẤT
    # =====================================================

    summary_keywords = [
        "tổng tiền xuất",
        "tổng giá trị xuất",
        "chi phí nguyên liệu xuất",
    ]

    if any(
        keyword in message_lower
        for keyword in summary_keywords
    ):
        return {
            "get_exports_summary_tool":
                create_exports_summary_tool(
                    authorization
                )
        }

    # =====================================================
    # CÔNG THỨC
    # =====================================================

    recipe_keywords = [
        "công thức",
        "công thức bánh",
    ]

    if any(
        keyword in message_lower
        for keyword in recipe_keywords
    ):
        return {
            "get_recipes_tool":
                create_recipes_tool(
                    authorization
                )
        }

    # =====================================================
    # FALLBACK
    # =====================================================

    return {
        "get_ingredients_tool":
            create_ingredients_tool(
                authorization
            ),

        "get_stock_tool":
            create_stock_tool(
                authorization
            ),

        "get_exports_single_tool":
            create_exports_single_tool(
                authorization
            ),

        "get_exports_recipe_tool":
            create_exports_recipe_tool(
                authorization
            ),

        "get_exports_summary_tool":
            create_exports_summary_tool(
                authorization
            ),

        "get_recipes_tool":
            create_recipes_tool(
                authorization
            ),

        "get_imports_tool":
            create_imports_tool(
                authorization
            ),
    }


def chat_with_ai(
    message: str,
    authorization: str,
    db: Session,
    conversation_id: int,
):
    # =====================================================
    # NGÀY HIỆN TẠI
    # =====================================================

    current_date = datetime.now().strftime(
        "%Y-%m-%d"
    )

    system_instruction = f"""
{SYSTEM_INSTRUCTION}

==================================================
NGÀY HIỆN TẠI
==================================================

Ngày hiện tại: {current_date}

Nếu người dùng chỉ cung cấp ngày và tháng
mà không có năm, sử dụng năm hiện tại.

Nếu người dùng cung cấp đầy đủ ngày, tháng, năm,
giữ nguyên năm đó.

Khi gọi tool, ngày phải có định dạng YYYY-MM-DD.
"""

    # =====================================================
    # LỊCH SỬ CONVERSATION
    # =====================================================

    history = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(
            Message.created_at.desc()
        )
        .limit(4)
        .all()
    )

    history.reverse()

    messages = [
        {
            "role": item.role,
            "content": item.content,
        }
        for item in history
        if item.role in [
            "user",
            "assistant",
        ]
    ]

    # =====================================================
    # MESSAGE HIỆN TẠI
    # =====================================================

    messages.append(
        {
            "role": "user",
            "content": message,
        }
    )

    # =====================================================
    # ROUTER / DISPATCHER
    # =====================================================

    route_result = dispatch_question(
        query=message,
        authorization=authorization,
        db=db,
    )

    route = route_result["route"]

    print("")
    print("================================")
    print(f"AI ROUTE: {route}")
    print("================================")

    # =====================================================
    # RAG
    # =====================================================

    if route == "RAG":

        return route_result["answer"]

    # =====================================================
    # BOTH → KNOWLEDGE CONTEXT
    # =====================================================

    rag_contexts = route_result.get(
        "contexts",
        []
    )

    if route == "BOTH" and rag_contexts:

        context_text = "\n\n".join(
            [
                (
                    f"[Knowledge {index}]\n"
                    f"Tiêu đề: {item['title']}\n"
                    f"Danh mục: {item['category']}\n"
                    f"Nội dung:\n"
                    f"{item['content']}"
                )
                for index, item in enumerate(
                    rag_contexts,
                    start=1,
                )
            ]
        )

        messages.insert(
            0,
            {
                "role": "system",
                "content": (
                    "KNOWLEDGE CONTEXT\n"
                    "=================\n\n"
                    f"{context_text}\n\n"
                    "=================\n"
                    "RULES\n"
                    "=================\n\n"
                    "Knowledge Context là nguồn duy nhất "
                    "cho kiến thức.\n"
                    "Tool Result là nguồn duy nhất "
                    "cho dữ liệu động.\n"
                    "Không bổ sung kiến thức ngoài Knowledge Context.\n"
                    "Không tự tạo số liệu, nhiệt độ, thời gian, "
                    "tần suất hoặc tiêu chuẩn.\n"
                    "Nếu Knowledge không có thông tin cần thiết, "
                    "nói rõ hệ thống chưa có thông tin.\n"
                    "Dữ liệu tồn kho phải lấy từ Tool Result."
                ),
            },
        )

    # =====================================================
    # TOOLS
    # =====================================================

    tools = select_tools_for_route(
        route=route,
        message=message,
        authorization=authorization,
    )

    print("")
    print(
        "🔧 Available tools:",
        ", ".join(tools.keys())
    )

    # =====================================================
    # AI PROVIDER
    # =====================================================

    manager = AIProviderManager(
        system_instruction=system_instruction,
        tools=tools,
        route=route,
    )

    return manager.chat(
        messages=messages
    )
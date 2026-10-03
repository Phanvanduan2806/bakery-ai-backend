from app.services.ai.providers.gemini import (
    ask_gemini,
)

from app.services.ai.providers.groq import (
    ask_groq,
)

from app.services.ai.providers.openrouter import (
    ask_openrouter,
)


ALLOWED_ROUTES = {
    "RAG",
    "TOOL",
    "BOTH",
    "CHAT",
}


ROUTER_PROMPT = """
Bạn là Router của AI Assistant
quản lý và vận hành tiệm bánh.

Nhiệm vụ của bạn là xác định câu hỏi
cần sử dụng nguồn dữ liệu nào.

==================================================
CÁC LOẠI ROUTE
==================================================

1. RAG

Sử dụng RAG khi câu hỏi yêu cầu
KIẾN THỨC hoặc HƯỚNG DẪN.

Ví dụ:

- Cách bảo quản bột mì?
- Men instant sử dụng như thế nào?
- Bột mì bị vón cục có dùng được không?
- Cách bảo quản nguyên liệu trong kho?
- Vì sao phải bảo quản nguyên liệu nơi khô ráo?
- Quy trình bảo quản nguyên liệu?
- Hướng dẫn sử dụng nguyên liệu?

Nếu người dùng hỏi về cách làm,
cách sử dụng, cách bảo quản hoặc xử lý
nguyên liệu thì ưu tiên RAG.

==================================================
2. TOOL
==================================================

Sử dụng TOOL khi câu hỏi yêu cầu
DỮ LIỆU THỰC TẾ / DỮ LIỆU HIỆN TẠI
từ hệ thống quản lý tiệm bánh.

Ví dụ:

- Kho còn bao nhiêu bột mì?
- Bột mì còn bao nhiêu?
- Hôm nay nhập bao nhiêu nguyên liệu?
- Hôm nay xuất bao nhiêu nguyên liệu?
- Tháng này nhập bao nhiêu?
- Có bao nhiêu công thức bánh?
- Danh sách nguyên liệu hiện tại?
- Nguyên liệu nào sắp hết?
- Nguyên liệu nào hết hàng?
- Doanh thu hôm nay bao nhiêu?

Nếu câu hỏi yêu cầu số lượng,
danh sách hoặc dữ liệu hiện tại
của hệ thống thì dùng TOOL.

QUAN TRỌNG:

"Có bao nhiêu công thức bánh?"
=> TOOL

Không chọn RAG chỉ vì câu hỏi
có từ "công thức".

==================================================
3. BOTH
==================================================

Sử dụng BOTH khi câu hỏi cần
CẢ dữ liệu thực tế từ TOOL
VÀ kiến thức từ RAG.

Ví dụ:

"Bột mì còn bao nhiêu và bảo quản thế nào?"
=> BOTH

"Kho còn 2kg bột mì thì bảo quản như thế nào?"
=> BOTH

"Những nguyên liệu sắp hết và cách bảo quản chúng?"
=> BOTH

Chỉ chọn BOTH khi câu hỏi thực sự
cần cả hai nguồn dữ liệu.

==================================================
4. CHAT
==================================================

Sử dụng CHAT cho hội thoại thông thường
không cần dữ liệu kho và không cần
knowledge từ RAG.

Ví dụ:

- Xin chào
- Cảm ơn bạn
- Bạn là ai?
- Chào buổi sáng

==================================================
QUY TẮC ƯU TIÊN
==================================================

Nếu câu hỏi chỉ cần dữ liệu hiện tại
từ hệ thống => TOOL.

Nếu câu hỏi chỉ cần kiến thức/hướng dẫn
=> RAG.

Nếu cần cả dữ liệu hiện tại và kiến thức
=> BOTH.

Nếu không cần dữ liệu hệ thống
và không cần knowledge => CHAT.

Không được chọn BOTH nếu câu hỏi
chỉ cần TOOL.

Không được chọn BOTH nếu câu hỏi
chỉ cần RAG.

==================================================
KẾT QUẢ
==================================================

Chỉ trả về đúng một trong bốn giá trị:

RAG
TOOL
BOTH
CHAT

Không giải thích.
Không thêm ký tự.
Không thêm markdown.

==================================================
CÂU HỎI NGƯỜI DÙNG
==================================================

{query}
"""


def _validate_route(
    result: str,
) -> str:

    result = result.strip().upper()

    result = result.replace(
        "```",
        "",
    ).strip()

    if result not in ALLOWED_ROUTES:
        raise ValueError(
            f"Router trả về kết quả không hợp lệ: {result}"
        )

    return result


def _classify_with_gemini(
    prompt: str,
) -> str:

    response = ask_gemini(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        system_instruction=(
            "Bạn là Router phân loại câu hỏi. "
            "Chỉ trả về RAG, TOOL, BOTH hoặc CHAT."
        ),
        tools=[],
    )

    if not response:
        raise ValueError(
            "Gemini không trả về kết quả Router."
        )

    return response

def _classify_with_groq(
    prompt: str,
) -> str:

    messages = [
        {
            "role": "system",
            "content": (
                "Bạn là Router phân loại câu hỏi. "
                "Chỉ trả về RAG, TOOL, BOTH hoặc CHAT."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    return ask_groq(
        messages,
        [],
        {},
    )


def _classify_with_openrouter(
    prompt: str,
) -> str:

    messages = [
        {
            "role": "system",
            "content": (
                "Bạn là Router phân loại câu hỏi. "
                "Chỉ trả về RAG, TOOL, BOTH hoặc CHAT."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    return ask_openrouter(
        messages,
        [],
        {},
    )

def classify_question(
    query: str,
) -> str:

    prompt = ROUTER_PROMPT.format(
        query=query,
    )

    providers = [
        (
            "Gemini",
            _classify_with_gemini,
        ),
        (
            "Groq",
            _classify_with_groq,
        ),
        (
            "OpenRouter",
            _classify_with_openrouter,
        ),
    ]

    for name, handler in providers:

        try:

            print("")
            print(
                f"🧭 Router {name}: đang phân loại..."
            )

            result = handler(
                prompt,
            )

            route = _validate_route(
                result,
            )

            print(
                f"✅ Router {name}: {route}"
            )

            return route

        except Exception as error:

            print(
                f"❌ Router {name}: FAILED"
            )

            print(
                f"   └─ {error}"
            )

    raise Exception(
        "Gemini, Groq và OpenRouter đều không thể phân loại câu hỏi."
    )
from app.services.ai.providers.gemini import (
    client,
)

from app.services.ai.providers.groq import (
    ask_groq,
)

from app.services.ai.providers.openrouter import (
    ask_openrouter,
)

from google.genai import types


RAG_SYSTEM_INSTRUCTION = """
Bạn là AI Assistant hỗ trợ quản lý
và vận hành tiệm bánh.

Hãy trả lời câu hỏi của người dùng
dựa trên KNOWLEDGE CONTEXT được cung cấp.

QUY TẮC:

1. Chỉ sử dụng thông tin có trong context.
2. Không tự bịa thêm thông tin.
3. Không sử dụng kiến thức bên ngoài context.
4. Nếu context không đủ thông tin để trả lời,
   hãy nói rõ rằng chưa tìm thấy thông tin phù hợp.
5. Trả lời bằng tiếng Việt.
6. Trả lời ngắn gọn, rõ ràng và thực tế.
"""


def _build_prompt(
    query: str,
    contexts: list[dict],
) -> str:

    context_text = "\n\n".join(
        [
            (
                f"[Knowledge {index}]\n"
                f"Tiêu đề: {item['title']}\n"
                f"Danh mục: {item['category']}\n"
                f"Nội dung:\n{item['content']}"
            )
            for index, item in enumerate(
                contexts,
                start=1,
            )
        ]
    )

    return f"""
KNOWLEDGE CONTEXT
=================

{context_text}

=================
CÂU HỎI
=================

{query}
"""


def _generate_with_gemini(
    prompt: str,
):

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=RAG_SYSTEM_INSTRUCTION,
            temperature=0.2,
        ),
    )

    if not response.text:
        raise ValueError(
            "Gemini không trả về nội dung."
        )

    return response.text


def _generate_with_groq(
    prompt: str,
):

    messages = [
        {
            "role": "system",
            "content": RAG_SYSTEM_INSTRUCTION,
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    result = ask_groq(
        messages,
        [],
        {},
    )

    if not result:
        raise ValueError(
            "Groq không trả về nội dung."
        )

    return result


def _generate_with_openrouter(
    prompt: str,
):

    messages = [
        {
            "role": "system",
            "content": RAG_SYSTEM_INSTRUCTION,
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    result = ask_openrouter(
        messages,
        [],
        {},
    )

    if not result:
        raise ValueError(
            "OpenRouter không trả về nội dung."
        )

    return result


def generate_rag_answer(
    query: str,
    contexts: list[dict],
):

    if not contexts:
        return (
            "Tôi không tìm thấy thông tin "
            "liên quan trong kho kiến thức."
        )

    prompt = _build_prompt(
        query=query,
        contexts=contexts,
    )

    providers = [
        (
            "Gemini",
            _generate_with_gemini,
        ),
        (
            "Groq",
            _generate_with_groq,
        ),
        (
            "OpenRouter",
            _generate_with_openrouter,
        ),
    ]

    for name, handler in providers:

        try:

            print("")
            print(
                f"🧠 RAG {name}: đang tạo câu trả lời..."
            )

            result = handler(
                prompt
            )

            print(
                f"✅ RAG {name}: 200 OK"
            )

            return result

        except Exception as error:

            print(
                f"❌ RAG {name}: FAILED"
            )

            print(
                f"   └─ {error}"
            )

    raise Exception(
        "Gemini, Groq và OpenRouter đều không thể tạo câu trả lời RAG."
    )
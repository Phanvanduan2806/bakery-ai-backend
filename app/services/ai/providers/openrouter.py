import os
import json
import traceback
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)


def ask_openrouter(
    messages,
    tools,
    tool_functions=None,
):
    """
    Gọi OpenRouter và xử lý tool calling.

    tool_functions:
        {
            "get_ingredients": function,
            "get_stock": function,
        }
    """

    if tool_functions is None:
        tool_functions = {}

    # =========================================================
    # LẦN 1: GỌI OPENROUTER
    # =========================================================

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    assistant_message = response.choices[0].message

    # =========================================================
    # KHÔNG CÓ TOOL CALL
    # =========================================================

    if not assistant_message.tool_calls:

        if not assistant_message.content:
            raise Exception(
                "OpenRouter không trả về nội dung."
            )

        return assistant_message.content

    # =========================================================
    # CÓ TOOL CALL
    # =========================================================

    messages.append(
        {
            "role": "assistant",
            "content": assistant_message.content,
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
                for tool_call in assistant_message.tool_calls
            ],
        }
    )

    # =========================================================
    # THỰC THI TOOLS
    # =========================================================

    for tool_call in assistant_message.tool_calls:

        function_name = tool_call.function.name
        arguments = tool_call.function.arguments

        print("")
        print(
            f"🔧 OpenRouter gọi tool: {function_name}"
        )

        try:
            function = tool_functions.get(
                function_name
            )

            if not function:
                raise Exception(
                    f"Tool không tồn tại: {function_name}"
                )

            if arguments:
                parsed_arguments = json.loads(
                    arguments
                )
            else:
                parsed_arguments = {}

            result = function(
                **parsed_arguments
            )

            print(
                f"✅ Tool {function_name}: OK"
            )

        except Exception as error:
            print(
                f"❌ Tool {function_name}: FAILED"
            )

            print(
                f"   └─ {type(error).__name__}: {error}"
            )

            traceback.print_exc()

            result = {
                "error": str(error)
            }

        # =====================================================
        # TRẢ KẾT QUẢ TOOL CHO OPENROUTER
        # =====================================================

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    result,
                    ensure_ascii=False,
                ),
            }
        )

    # =========================================================
    # LẦN 2: OPENROUTER TẠO CÂU TRẢ LỜI CUỐI
    # =========================================================

    print("")
    print(
        "🤖 OpenRouter: đang xử lý kết quả tool..."
    )

    final_response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    final_message = (
        final_response.choices[0].message
    )

    if not final_message.content:
        raise Exception(
            "OpenRouter không trả về câu trả lời cuối."
        )

    return final_message.content

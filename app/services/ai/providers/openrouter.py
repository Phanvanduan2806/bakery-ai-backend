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
    tool_choice="auto",
):
    """
    Gọi OpenRouter và xử lý Tool Calling.

    tool_choice:
        auto
            Model tự quyết định có gọi tool hay không.

        required
            Model bắt buộc phải gọi ít nhất một tool.
    """

    if tool_functions is None:
        tool_functions = {}

    # Không sửa trực tiếp list messages bên ngoài.
    request_messages = list(messages)

    # =========================================================
    # LẦN 1: OPENROUTER
    # =========================================================

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=request_messages,
        tools=tools,
        tool_choice=tool_choice,
    )

    # Log model thực tế được OpenRouter sử dụng
    print(
        f"🔎 OpenRouter model: "
        f"{getattr(response, 'model', 'unknown')}"
    )

    assistant_message = (
        response.choices[0].message
    )

    tool_calls = (
        assistant_message.tool_calls
        or []
    )

    # =========================================================
    # KHÔNG CÓ TOOL CALL
    # =========================================================

    if not tool_calls:

        if tool_choice == "required":

            raise Exception(
                "OpenRouter không gọi tool "
                "mặc dù tool_choice=required."
            )

        if not assistant_message.content:

            raise Exception(
                "OpenRouter không trả về nội dung."
            )

        return assistant_message.content

    # =========================================================
    # CÓ TOOL CALL
    # =========================================================

    print(
        f"🔧 OpenRouter: nhận "
        f"{len(tool_calls)} tool call(s)"
    )

    request_messages.append(
        {
            "role": "assistant",
            "content": (
                assistant_message.content
                or ""
            ),
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": (
                            tool_call.function.name
                        ),
                        "arguments": (
                            tool_call.function.arguments
                            or "{}"
                        ),
                    },
                }
                for tool_call in tool_calls
            ],
        }
    )

    # =========================================================
    # THỰC THI TOOLS
    # =========================================================

    for tool_call in tool_calls:

        function_name = (
            tool_call.function.name
        )

        arguments = (
            tool_call.function.arguments
            or "{}"
        )

        print("")
        print(
            f"🔧 OpenRouter gọi tool: "
            f"{function_name}"
        )

        try:

            function = tool_functions.get(
                function_name
            )

            if not function:

                raise Exception(
                    f"Tool không tồn tại: "
                    f"{function_name}"
                )

            parsed_arguments = json.loads(
                arguments
            )

            if not isinstance(
                parsed_arguments,
                dict,
            ):
                raise Exception(
                    "Tool arguments phải là object."
                )

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
                f"   └─ "
                f"{type(error).__name__}: "
                f"{error}"
            )

            traceback.print_exc()

            result = {
                "error": str(error)
            }

        # =====================================================
        # TRẢ TOOL RESULT CHO OPENROUTER
        # =====================================================

        request_messages.append(
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
    # LẦN 2: TẠO CÂU TRẢ LỜI CUỐI
    # =========================================================

    print("")
    print(
        "🤖 OpenRouter: đang xử lý "
        "kết quả tool..."
    )

    final_response = (
        client.chat.completions.create(
            model="openrouter/free",
            messages=request_messages,
            tools=tools,
            # Sau khi đã có tool result,
            # KHÔNG ép gọi tool lần nữa.
            tool_choice="auto",
        )
    )

    print(
        f"🔎 OpenRouter final model: "
        f"{getattr(final_response, 'model', 'unknown')}"
    )

    final_message = (
        final_response.choices[0].message
    )

    if not final_message.content:

        raise Exception(
            "OpenRouter không trả về "
            "câu trả lời cuối."
        )

    return final_message.content
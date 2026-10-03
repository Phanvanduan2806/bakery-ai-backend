import os
import json
import traceback

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_groq(
    messages,
    tools,
    tool_functions=None,
    tool_choice="auto",
):
    """
    Gọi Groq và xử lý Tool Calling.

    tool_choice:
        auto
            Model tự quyết định có gọi tool hay không.

        required
            Model bắt buộc phải gọi ít nhất một tool.
    """

    if tool_functions is None:
        tool_functions = {}

    # =========================================================
    # LẦN 1: GỌI GROQ
    # =========================================================

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=tools,
        tool_choice=tool_choice,
    )

    assistant_message = (
        response.choices[0].message
    )

    # =========================================================
    # KHÔNG CÓ TOOL CALL
    # =========================================================

    if not assistant_message.tool_calls:

        if tool_choice == "required":

            raise Exception(
                "Groq không gọi tool "
                "mặc dù tool_choice=required."
            )

        if not assistant_message.content:

            raise Exception(
                "Groq không trả về nội dung."
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
                        "name": (
                            tool_call.function.name
                        ),
                        "arguments": (
                            tool_call.function.arguments
                        ),
                    },
                }
                for tool_call
                in assistant_message.tool_calls
            ],
        }
    )

    # =========================================================
    # THỰC THI TOOLS
    # =========================================================

    for tool_call in (
        assistant_message.tool_calls
    ):

        function_name = (
            tool_call.function.name
        )

        arguments = (
            tool_call.function.arguments
        )

        print("")
        print(
            f"🔧 Groq gọi tool: "
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
                f"   └─ "
                f"{type(error).__name__}: "
                f"{error}"
            )

            traceback.print_exc()

            result = {
                "error": str(error)
            }

        # =====================================================
        # TRẢ KẾT QUẢ TOOL CHO GROQ
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
    # LẦN 2: GROQ TẠO CÂU TRẢ LỜI CUỐI
    # =========================================================

    print("")
    print(
        "🤖 Groq: đang xử lý "
        "kết quả tool..."
    )

    final_response = (
        client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )
    )

    final_message = (
        final_response.choices[0].message
    )

    if not final_message.content:

        raise Exception(
            "Groq không trả về "
            "câu trả lời cuối."
        )

    return final_message.content
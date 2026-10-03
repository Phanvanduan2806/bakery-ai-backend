import os
import traceback

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(
    messages,
    system_instruction: str,
    tools,
    tool_functions=None,
    tool_choice="auto",
):
    """
    Gọi Gemini và xử lý Tool Calling.

    tool_choice:
        auto
            Gemini tự quyết định có gọi tool hay không.

        required
            Gemini bắt buộc phải gọi ít nhất một tool.
            Được map sang FunctionCallingConfig(mode="ANY").
    """

    if tool_functions is None:
        tool_functions = {}

    # =========================================================
    # TOOL CONFIG
    # =========================================================

    tool_config = None

    if tools:

        if tool_choice == "required":

            tool_config = types.ToolConfig(
                function_calling_config=types.FunctionCallingConfig(
                    mode="ANY",
                )
            )

        else:

            tool_config = types.ToolConfig(
                function_calling_config=types.FunctionCallingConfig(
                    mode="AUTO",
                )
            )

    # =========================================================
    # CHUYỂN MESSAGES SANG FORMAT GEMINI
    # =========================================================

    contents = []

    for message in messages:

        role = message["role"]
        content = message.get("content")

        if role == "user":
            gemini_role = "user"

        elif role == "assistant":
            gemini_role = "model"

        else:
            continue

        if not content:
            continue

        contents.append(
            types.Content(
                role=gemini_role,
                parts=[
                    types.Part(
                        text=content
                    )
                ],
            )
        )

    # =========================================================
    # CONFIG
    # =========================================================

    config_kwargs = {
        "system_instruction": system_instruction,
        "tools": tools,
    }

    if tool_config is not None:
        config_kwargs["tool_config"] = tool_config

    config = types.GenerateContentConfig(
        **config_kwargs
    )

    # =========================================================
    # LẦN GỌI ĐẦU TIÊN
    # =========================================================

    print("")
    print("🤖 Gemini: đang gọi...")

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config=config,
    )

    # =========================================================
    # KIỂM TRA TOOL CALL
    # =========================================================

    function_calls = []

    if response.candidates:

        candidate = response.candidates[0]

        if candidate.content:

            for part in candidate.content.parts:

                if part.function_call:

                    function_calls.append(
                        part.function_call
                    )

    # =========================================================
    # KHÔNG CÓ TOOL CALL
    # =========================================================

    if not function_calls:

        if not response.text:
            raise Exception(
                "Gemini không trả về nội dung."
            )

        # Với required mà Gemini không gọi tool
        # thì coi như provider thất bại.
        if tool_choice == "required":

            raise Exception(
                "Gemini không thực hiện Tool Calling "
                "mặc dù tool_choice=required."
            )

        print("✅ Gemini: 200 OK")

        return response.text

    # =========================================================
    # CÓ TOOL CALL
    # =========================================================

    print(
        f"🔧 Gemini yêu cầu "
        f"{len(function_calls)} tool"
    )

    # Lưu response của Gemini vào conversation
    contents.append(
        response.candidates[0].content
    )

    # =========================================================
    # THỰC THI TOOLS
    # =========================================================

    tool_response_parts = []

    for function_call in function_calls:

        function_name = function_call.name

        arguments = dict(
            function_call.args or {}
        )

        print("")
        print(
            f"🔧 Gemini gọi tool: "
            f"{function_name}"
        )

        print(
            f"   Arguments: {arguments}"
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

            result = function(
                **arguments
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
        # CHUẨN BỊ TOOL RESPONSE
        # =====================================================

        tool_response_parts.append(
            types.Part(
                function_response=types.FunctionResponse(
                    name=function_name,
                    response={
                        "result": result
                    },
                )
            )
        )

    # =========================================================
    # GỬI TOOL RESULT CHO GEMINI
    # =========================================================

    contents.append(
        types.Content(
            role="user",
            parts=tool_response_parts,
        )
    )

    # =========================================================
    # LẦN GỌI THỨ 2
    # =========================================================

    print("")
    print(
        "🤖 Gemini: đang xử lý "
        "kết quả tool..."
    )

    final_response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config=config,
    )

    if not final_response.text:

        raise Exception(
            "Gemini không trả về "
            "câu trả lời cuối."
        )

    print(
        "✅ Gemini: final answer"
    )

    return final_response.text
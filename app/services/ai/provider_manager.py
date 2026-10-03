from app.services.ai.schemas import TOOLS_SCHEMA

from app.services.ai.providers.gemini import (
    ask_gemini,
)

from app.services.ai.providers.groq import (
    ask_groq,
)

from app.services.ai.providers.openrouter import (
    ask_openrouter,
)


class AIProviderManager:

    def __init__(
        self,
        system_instruction: str,
        tools: dict,
        route: str = "CHAT",
    ):
        self.system_instruction = system_instruction
        self.tools = tools
        self.route = route

    def chat(
        self,
        messages: list,
    ):

        providers = [
            {
                "name": "Gemini",
                "handler": self._call_gemini,
            },
            {
                "name": "Groq",
                "handler": self._call_groq,
            },
            {
                "name": "OpenRouter",
                "handler": self._call_openrouter,
            },
        ]

        for provider in providers:

            try:

                print("")
                print(
                    f"🤖 {provider['name']}: đang gọi..."
                )

                response = provider["handler"](
                    messages
                )

                if not response:
                    raise Exception(
                        f"{provider['name']} "
                        "không trả về nội dung."
                    )

                print(
                    f"✅ {provider['name']}: 200 OK"
                )

                return response

            except Exception as error:

                print(
                    f"❌ {provider['name']}: FAILED"
                )

                print(
                    f"   └─ {error}"
                )

        print("")
        print(
            "❌ Tất cả AI provider đều FAILED"
        )

        raise Exception(
            "Gemini, Groq và OpenRouter "
            "đều không khả dụng."
        )

    def _get_tool_choice(self):
        """
        TOOL / BOTH:
            Bắt buộc model phải sử dụng tool.

        CHAT:
            Cho phép model tự quyết định.

        RAG:
            Không đi qua ProviderManager.
        """

        if self.route in [
            "TOOL",
            "BOTH",
        ]:
            return "required"

        return "auto"

    def _call_gemini(
        self,
        messages: list,
    ):

        response = ask_gemini(
            messages,
            self.system_instruction,
            list(self.tools.values()),
            tool_functions=self.tools,
            tool_choice=self._get_tool_choice(),
        )

        if not response.text:
            raise Exception(
                "Gemini không trả về nội dung."
            )

        return response.text

    def _call_groq(
        self,
        messages: list,
    ):

        provider_messages = [
            {
                "role": "system",
                "content": self.system_instruction,
            },
            *messages,
        ]

        return ask_groq(
            provider_messages,
            TOOLS_SCHEMA,
            tool_functions=self.tools,
            tool_choice=self._get_tool_choice(),
        )

    def _call_openrouter(
        self,
        messages: list,
    ):

        provider_messages = [
            {
                "role": "system",
                "content": self.system_instruction,
            },
            *messages,
        ]

        return ask_openrouter(
            provider_messages,
            TOOLS_SCHEMA,
            tool_functions=self.tools,
            tool_choice=self._get_tool_choice(),
        )
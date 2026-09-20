import os

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
):

    contents = []

    for message in messages:

        role = message["role"]
        content = message["content"]

        if role == "user":
            gemini_role = "user"

        elif role == "assistant":
            gemini_role = "model"

        else:
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

    return client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=tools,
        ),
    )
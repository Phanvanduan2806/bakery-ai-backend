import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


# =========================================================
# ENV
# =========================================================

load_dotenv()


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# =========================================================
# EMBEDDING CONFIG
# =========================================================

EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIMENSION = 768


# =========================================================
# EMBEDDING DOCUMENT
# =========================================================

def embed_document(
    title: str,
    content: str,
) -> list[float]:

    text = (
        f"title: {title} | "
        f"text: {content}"
    )

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSION,
        ),
    )

    embedding = response.embeddings[0].values

    if not embedding:
        raise ValueError(
            "Gemini không trả về embedding"
        )

    return embedding


# =========================================================
# EMBEDDING QUERY
# =========================================================

def embed_query(
    query: str,
) -> list[float]:

    text = (
        f"task: search result | "
        f"query: {query}"
    )

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(
            output_dimensionality=EMBEDDING_DIMENSION,
        ),
    )

    embedding = response.embeddings[0].values

    if not embedding:
        raise ValueError(
            "Gemini không trả về query embedding"
        )

    return embedding
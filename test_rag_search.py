from app.database import SessionLocal

from app.services.ai.rag.search import (
    search_knowledge,
)


AUTHORIZATION = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3ODk3MjUyNjMsImV4cCI6MTc5MDMzMDA2MywiZGF0YSI6eyJ1c2VyX2lkIjo1fX0.PM-mvTSw3wCBBuPdR3rhUxlq5IhV-EcXS_J_GH2h-3k"


db = SessionLocal()

try:

    results = search_knowledge(
        query="Bột mì nên bảo quản như thế nào?",
        authorization=AUTHORIZATION,
        db=db,
        limit=5,
    )

    for index, item in enumerate(
        results,
        start=1,
    ):

        print(f"\nRESULT {index}")
        print("Title:", item["title"])
        print("Category:", item["category"])
        print("Chunk:", item["chunk_index"])
        print("Distance:", item["distance"])
        print("Content:", item["content"])

finally:

    db.close()
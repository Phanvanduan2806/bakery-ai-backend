from app.database import SessionLocal

from app.services.ai.rag.search import (
    search_knowledge,
)

from app.services.ai.rag.generate import (
    generate_rag_answer,
)


AUTHORIZATION = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3ODk3MjUyNjMsImV4cCI6MTc5MDMzMDA2MywiZGF0YSI6eyJ1c2VyX2lkIjo1fX0.PM-mvTSw3wCBBuPdR3rhUxlq5IhV-EcXS_J_GH2h-3k"


query = "Thời tiết hôm nay như thế nào?"


db = SessionLocal()

try:

    # ==========================================
    # Retrieval
    # ==========================================

    contexts = search_knowledge(
        query=query,
        authorization=AUTHORIZATION,
        db=db,
        limit=5,
    )

    print(
        f"Tìm được {len(contexts)} contexts"
    )

    # ==========================================
    # Generation
    # ==========================================

    answer = generate_rag_answer(
        query=query,
        contexts=contexts,
    )

    print("\n==============================")
    print("AI ANSWER")
    print("==============================")
    print(answer)

finally:

    db.close()
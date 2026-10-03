from app.database import SessionLocal

from app.services.ai.dispatcher import (
    dispatch_question,
)



AUTHORIZATION = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3ODk3MjUyNjMsImV4cCI6MTc5MDMzMDA2MywiZGF0YSI6eyJ1c2VyX2lkIjo1fX0.PM-mvTSw3wCBBuPdR3rhUxlq5IhV-EcXS_J_GH2h-3k"


questions = [
    "Bột mì nên bảo quản thế nào?",
    "Kho còn bao nhiêu bột mì?",
    "Bột mì còn bao nhiêu và bảo quản thế nào?",
    "Xin chào",
]


db = SessionLocal()

try:

    for question in questions:

        result = dispatch_question(
            query=question,
            authorization=AUTHORIZATION,
            db=db,
        )

        print(
            "================================"
        )

        print(
            f"Question: {question}"
        )

        print(
            f"Route: {result['route']}"
        )

        print(
            f"Contexts: {len(result['contexts'])}"
        )

        if result["answer"]:
            print(
                f"Answer: {result['answer']}"
            )

finally:

    db.close()

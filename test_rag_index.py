from app.database import SessionLocal

from app.services.ai.rag.index import (
    index_knowledge,
)


AUTHORIZATION = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3ODk3MjUyNjMsImV4cCI6MTc5MDMzMDA2MywiZGF0YSI6eyJ1c2VyX2lkIjo1fX0.PM-mvTSw3wCBBuPdR3rhUxlq5IhV-EcXS_J_GH2h-3k"


db = SessionLocal()

try:

    result = index_knowledge(
        authorization=AUTHORIZATION,
        db=db,
    )

    print(result)

finally:

    db.close()
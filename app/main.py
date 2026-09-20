from fastapi import FastAPI

from app.database import Base, engine
from app.models import Conversation, Message
from app.routers import ai, conversations


# Tạo các bảng database nếu chưa tồn tại
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Bakery AI",
    description="AI Assistant for Bakery Inventory",
    version="1.0.0",
)


app.include_router(ai.router)
app.include_router(conversations.router)


@app.get("/")
def root():
    return {
        "message": "Bakery AI is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
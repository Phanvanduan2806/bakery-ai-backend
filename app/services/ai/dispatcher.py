from sqlalchemy.orm import Session

from app.services.ai.router import (
    classify_question,
)

from app.services.ai.rag import (
    search_knowledge,
    generate_rag_answer,
)


def dispatch_question(
    query: str,
    authorization: str,
    db: Session,
):
    """
    Điều phối câu hỏi dựa trên route:

    RAG
        -> RAG retrieval + generation

    TOOL
        -> trả về route để chat.py
           tiếp tục xử lý Tool Calling

    BOTH
        -> RAG retrieval
        -> đồng thời báo cho chat.py
           cần xử lý Tool

    CHAT
        -> trả về route để chat.py
           xử lý hội thoại bình thường
    """

    route = classify_question(
        query
    )

    # ==========================================
    # RAG
    # ==========================================

    if route == "RAG":

        contexts = search_knowledge(
            query=query,
            authorization=authorization,
            db=db,
            limit=5,
        )

        answer = generate_rag_answer(
            query=query,
            contexts=contexts,
        )

        return {
            "route": "RAG",
            "answer": answer,
            "contexts": contexts,
        }

    # ==========================================
    # TOOL
    # ==========================================

    if route == "TOOL":

        return {
            "route": "TOOL",
            "answer": None,
            "contexts": [],
        }

    # ==========================================
    # BOTH
    # ==========================================

    if route == "BOTH":

        contexts = search_knowledge(
            query=query,
            authorization=authorization,
            db=db,
            limit=3,
        )

        return {
            "route": "BOTH",
            "answer": None,
            "contexts": contexts,
        }

    # ==========================================
    # CHAT
    # ==========================================

    if route == "CHAT":

        return {
            "route": "CHAT",
            "answer": None,
            "contexts": [],
        }

    raise ValueError(
        f"Route không hợp lệ: {route}"
    )

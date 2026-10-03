from sqlalchemy.orm import Session

from app.models.knowledge import (
    KnowledgeDocument,
    KnowledgeChunk,
)

from app.services.kho.user import (
    get_current_user,
)

from app.services.ai.rag.embedding import (
    embed_query,
)


def search_knowledge(
    query: str,
    authorization: str,
    db: Session,
    limit: int = 5,
    max_distance: float = 0.25,
):
    """
    Tìm các knowledge chunk liên quan
    bằng vector similarity.

    max_distance:
        Ngưỡng khoảng cách cosine.
        Distance càng nhỏ thì nội dung càng liên quan.

        Ví dụ:
            0.10 -> rất giống
            0.20 -> khá liên quan
            0.25 -> ngưỡng mặc định
            > 0.25 -> không lấy
    """

    # ==========================================
    # 1. Lấy thông tin user
    # ==========================================

    user = get_current_user(
        authorization
    )

    branch_id = user.get(
        "current_branch"
    )

    if branch_id is None:
        branch_id = user.get(
            "branch_id"
        )

    if branch_id is None:
        raise ValueError(
            "Không xác định được branch_id"
        )

    branch_id = int(
        branch_id
    )

    # ==========================================
    # 2. Tạo embedding cho câu hỏi
    # ==========================================

    query_embedding = embed_query(
        query
    )

    # ==========================================
    # 3. Tính cosine distance
    # ==========================================

    distance = KnowledgeChunk.embedding.cosine_distance(
        query_embedding
    )

    # ==========================================
    # 4. Vector similarity search
    # ==========================================

    results = (
        db.query(
            KnowledgeChunk,
            KnowledgeDocument,
            distance.label("distance"),
        )
        .join(
            KnowledgeDocument,
            KnowledgeChunk.document_id
            == KnowledgeDocument.id,
        )
        .filter(
            KnowledgeDocument.branch_id
            == branch_id
        )
        .filter(
            KnowledgeDocument.status
            == "publish"
        )
        .filter(
            distance <= max_distance
        )
        .order_by(
            distance.asc()
        )
        .limit(limit)
        .all()
    )

    # ==========================================
    # 5. Format kết quả
    # ==========================================

    output = []

    for (
        chunk,
        document,
        similarity_distance,
    ) in results:

        output.append(
            {
                "document_id": document.id,
                "knowledge_id": document.knowledge_id,
                "branch_id": document.branch_id,
                "title": document.title,
                "category": document.category,
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
                "distance": float(
                    similarity_distance
                ),
            }
        )

    return output

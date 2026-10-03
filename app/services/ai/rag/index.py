from sqlalchemy.orm import Session

from app.models.knowledge import (
    KnowledgeDocument,
    KnowledgeChunk,
)

from app.services.kho.knowledge import get_knowledge

from app.services.ai.rag.embedding import (
    embed_document,
)


def split_into_chunks(
    content: str,
) -> list[str]:
    """
    Chia knowledge thành các đoạn nhỏ.
    Hiện tại chia theo paragraph.
    """

    chunks = [
        paragraph.strip()
        for paragraph in content.split("\n\n")
        if paragraph.strip()
    ]

    return chunks


def index_knowledge(
    authorization: str,
    db: Session,
):
    """
    Đồng bộ knowledge từ WordPress
    vào PostgreSQL + pgvector.
    """

    knowledge_list = get_knowledge(
        authorization
    )

    indexed_documents = 0
    indexed_chunks = 0

    try:

        for item in knowledge_list:

            # Chỉ index knowledge đã publish
            if item.get("status") != "publish":
                continue

            knowledge_id = int(
                item["id"]
            )

            branch_id = int(
                item["branch_id"]
            )

            title = item.get(
                "title",
                ""
            ).strip()

            content = item.get(
                "content",
                ""
            ).strip()

            category = item.get(
                "category"
            )

            if not content:
                continue

            # =====================================
            # Tìm document đã tồn tại
            # =====================================

            document = (
                db.query(KnowledgeDocument)
                .filter(
                    KnowledgeDocument.knowledge_id
                    == knowledge_id
                )
                .first()
            )

            if document:

                document.branch_id = branch_id
                document.title = title
                document.category = category
                document.status = item.get(
                    "status"
                )

                # Xóa chunk cũ
                db.query(KnowledgeChunk).filter(
                    KnowledgeChunk.document_id
                    == document.id
                ).delete(
                    synchronize_session=False
                )

            else:

                document = KnowledgeDocument(
                    knowledge_id=knowledge_id,
                    branch_id=branch_id,
                    title=title,
                    category=category,
                    status=item.get("status"),
                )

                db.add(document)

                # Lấy document.id
                db.flush()

            # =====================================
            # Chia thành chunks
            # =====================================

            chunks = split_into_chunks(
                content
            )

            # =====================================
            # Tạo embedding + lưu chunk
            # =====================================

            for chunk_index, chunk_content in enumerate(
                chunks
            ):

                embedding = embed_document(
                    title=title,
                    content=chunk_content,
                )

                chunk = KnowledgeChunk(
                    document_id=document.id,
                    chunk_index=chunk_index,
                    content=chunk_content,
                    embedding=embedding,
                )

                db.add(chunk)

                indexed_chunks += 1

            indexed_documents += 1

        db.commit()

    except Exception:
        db.rollback()
        raise

    return {
        "success": True,
        "documents": indexed_documents,
        "chunks": indexed_chunks,
    }
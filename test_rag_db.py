from app.database import SessionLocal

from app.models.knowledge import (
    KnowledgeDocument,
    KnowledgeChunk,
)


db = SessionLocal()

try:

    documents = (
        db.query(KnowledgeDocument)
        .all()
    )

    chunks = (
        db.query(KnowledgeChunk)
        .all()
    )

    print(
        "Documents:",
        len(documents)
    )

    print(
        "Chunks:",
        len(chunks)
    )

    for document in documents:

        print("\nDOCUMENT")
        print(
            "ID:",
            document.id
        )
        print(
            "Knowledge ID:",
            document.knowledge_id
        )
        print(
            "Branch ID:",
            document.branch_id
        )
        print(
            "Title:",
            document.title
        )
        print(
            "Category:",
            document.category
        )

    for chunk in chunks:

        print("\nCHUNK")
        print(
            "ID:",
            chunk.id
        )
        print(
            "Document ID:",
            chunk.document_id
        )
        print(
            "Chunk index:",
            chunk.chunk_index
        )
        print(
            "Content:",
            chunk.content[:100]
        )
        print(
            "Embedding dimension:",
            len(chunk.embedding)
        )

finally:

    db.close()
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.database import Base


class KnowledgeDocument(Base):
    __tablename__ = "ai_knowledge_documents"

    id = Column(Integer, primary_key=True, index=True)

    # ID của knowledge bên WordPress
    knowledge_id = Column(
        Integer,
        unique=True,
        nullable=False,
        index=True,
    )

    branch_id = Column(
        Integer,
        nullable=False,
        index=True,
    )

    title = Column(
        String(500),
        nullable=False,
    )

    category = Column(
        String(255),
        nullable=True,
    )

    status = Column(
        String(50),
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    chunks = relationship(
        "KnowledgeChunk",
        back_populates="document",
        cascade="all, delete-orphan",
    )


class KnowledgeChunk(Base):
    __tablename__ = "ai_knowledge_chunks"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    document_id = Column(
        Integer,
        ForeignKey(
            "ai_knowledge_documents.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    chunk_index = Column(
        Integer,
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    embedding = Column(
        Vector(768),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    document = relationship(
        "KnowledgeDocument",
        back_populates="chunks",
    )
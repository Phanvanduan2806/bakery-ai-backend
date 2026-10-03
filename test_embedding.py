from app.services.ai.rag import embed_document


text = embed_document(
    title="Bảo quản bột mì",
    content=(
        "Bột mì cần được bảo quản ở nơi khô ráo, "
        "thoáng mát và tránh ánh nắng trực tiếp."
    ),
)


print("Embedding dimension:", len(text))
print("First 10 values:", text[:10])
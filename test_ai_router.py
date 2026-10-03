from app.services.ai.router import (
    classify_question,
)


questions = [
    "Kho còn bao nhiêu bột mì?",
    "Hôm nay nhập bao nhiêu nguyên liệu?",
    "Bột mì còn bao nhiêu?",
    "Bột mì còn bao nhiêu và bảo quản thế nào?",
    "Bột mì bị vón cục có dùng được không?",
    "Cách bảo quản nguyên liệu trong kho?",
    "Có bao nhiêu công thức bánh?",
    "Xin chào",
]


for question in questions:

    result = classify_question(
        question
    )

    print(question)

    print(
        f"  -> {result}"
    )

    print()

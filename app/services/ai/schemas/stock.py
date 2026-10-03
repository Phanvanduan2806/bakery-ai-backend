STOCK_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_stock_tool",
        "description": (
            "Tra cứu tồn kho. "
            "Dùng ingredient_name khi hỏi một nguyên liệu cụ thể. "
            "Dùng status='low' để tìm nguyên liệu gần hết, "
            "status='out' để tìm nguyên liệu đã hết. "
            "Để trống cả hai để xem toàn bộ tồn kho."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "ingredient_name": {
                    "type": "string",
                    "description": (
                        "Tên nguyên liệu; để rỗng khi tìm nhiều nguyên liệu."
                    ),
                },
                "status": {
                    "type": "string",
                    "enum": ["", "low", "out"],
                    "description": (
                        "low = gần hết; out = đã hết; "
                        "rỗng = không lọc trạng thái."
                    ),
                },
            },
            "required": [],
        },
    },
}
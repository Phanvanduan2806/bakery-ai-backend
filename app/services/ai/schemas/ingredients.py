
INGREDIENTS_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_ingredients_tool",

        "description": (
            "Tìm thông tin của một nguyên liệu theo tên, "
            "bao gồm thông tin nguyên liệu và giá. "
            "KHÔNG dùng tool này để kiểm tra số lượng tồn kho."
        ),

        "parameters": {
            "type": "object",

            "properties": {
                "ingredient_name": {
                    "type": "string",
                    "description": (
                        "Tên nguyên liệu cần tìm. "
                        "Ví dụ: cà rốt, bột mì, đường."
                    ),
                },
            },

            "required": [
                "ingredient_name"
            ],
        },
    },
}

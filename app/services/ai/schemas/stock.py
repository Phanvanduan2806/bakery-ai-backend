STOCK_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_stock_tool",

        "description": (
            "Tra cứu tồn kho nguyên liệu. "

            "Nếu người dùng hỏi về một nguyên liệu cụ thể "
            "như 'bột mì còn bao nhiêu' hoặc "
            "'đường còn không', hãy truyền ingredient_name. "

            "Nếu người dùng hỏi dạng liệt kê như "
            "'nguyên liệu nào sắp hết', "
            "'những nguyên liệu nào gần hết', "
            "'liệt kê nguyên liệu sắp hết', "
            "thì KHÔNG cần ingredient_name. "
            "Hãy gọi tool với ingredient_name rỗng "
            "và status='low'. "

            "Nếu người dùng hỏi nguyên liệu nào đã hết "
            "hoặc hết hàng, gọi tool với status='out'. "

            "Nếu người dùng yêu cầu liệt kê toàn bộ tồn kho, "
            "có thể gọi tool với cả ingredient_name và status "
            "để trống. "

            "KHÔNG hỏi lại tên nguyên liệu khi người dùng "
            "đang yêu cầu tìm hoặc liệt kê một nhóm nguyên liệu."
        ),

        "parameters": {
            "type": "object",

            "properties": {
                "ingredient_name": {
                    "type": "string",
                    "description": (
                        "Tên nguyên liệu cần kiểm tra. "
                        "Để chuỗi rỗng nếu người dùng muốn "
                        "kiểm tra nhiều nguyên liệu hoặc "
                        "liệt kê theo trạng thái."
                    ),
                },

                "status": {
                    "type": "string",
                    "enum": [
                        "",
                        "low",
                        "out",
                    ],
                    "description": (
                        "'low' = nguyên liệu gần hết. "
                        "'out' = nguyên liệu đã hết. "
                        "Để rỗng nếu không cần lọc "
                        "theo trạng thái."
                    ),
                },
            },

            "required": [],
        },
    },
}

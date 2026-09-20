EXPORTS_RECIPE_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_exports_recipe_tool",
        "description": (
            "Tra cứu lịch sử xuất kho theo công thức. "
            "Có thể tìm theo tên công thức, "
            "khoảng thời gian và giới hạn số kết quả."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "recipe_name": {
                    "type": "string",
                    "description": (
                        "Tên công thức cần tìm. "
                        "Để trống nếu muốn xem tất cả."
                    ),
                },
                "from_date": {
                    "type": "string",
                    "description": (
                        "Ngày bắt đầu theo định dạng YYYY-MM-DD. "
                        "Để trống nếu không giới hạn."
                    ),
                },
                "to_date": {
                    "type": "string",
                    "description": (
                        "Ngày kết thúc theo định dạng YYYY-MM-DD. "
                        "Để trống nếu không giới hạn."
                    ),
                },
                "limit": {
                    "type": "integer",
                    "description": (
                        "Số lượng kết quả tối đa. "
                        "Mặc định 20."
                    ),
                    "default": 20,
                },
            },
            "required": [],
        },
    },
}


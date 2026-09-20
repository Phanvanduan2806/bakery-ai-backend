EXPORTS_SUMMARY_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_exports_summary_tool",
        "description": (
            "Tính tổng tiền nguyên liệu đã xuất kho "
            "trong một khoảng thời gian. "
            "Bao gồm cả xuất kho lẻ và xuất kho theo công thức."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "from_date": {
                    "type": "string",
                    "description": (
                        "Ngày bắt đầu theo định dạng YYYY-MM-DD."
                    ),
                },
                "to_date": {
                    "type": "string",
                    "description": (
                        "Ngày kết thúc theo định dạng YYYY-MM-DD."
                    ),
                },
            },
            "required": [],
        },
    },
}
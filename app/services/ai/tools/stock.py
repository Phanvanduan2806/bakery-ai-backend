from app.services.kho import find_stock


def create_stock_tool(
    authorization: str,
):
    def get_stock_tool(
        ingredient_name: str = "",
        status: str = "",
    ) -> dict:
        """
        Tra cứu tồn kho.

        Có thể dùng theo 4 trường hợp:

        1. Có tên nguyên liệu:
           → tìm tồn kho của nguyên liệu đó.

        2. Không có tên + status="low":
           → tìm tất cả nguyên liệu gần hết.

        3. Không có tên + status="out":
           → tìm tất cả nguyên liệu đã hết.

        4. Không có tên + không có status:
           → trả về toàn bộ tồn kho.
        """

        results = find_stock(
            authorization=authorization,
            ingredient_name=ingredient_name,
            status=status,
        )

        # ================================================
        # KHÔNG CÓ KẾT QUẢ
        # ================================================

        if not results:

            if status == "low":
                message = (
                    "Không tìm thấy nguyên liệu nào "
                    "đang gần hết."
                )

            elif status == "out":
                message = (
                    "Không tìm thấy nguyên liệu nào "
                    "đã hết."
                )

            elif ingredient_name:
                message = (
                    f"Không tìm thấy tồn kho "
                    f"của '{ingredient_name}'."
                )

            else:
                message = "Không có dữ liệu tồn kho."

            return {
                "found": False,
                "ingredient_name": ingredient_name,
                "status": status,
                "message": message,
            }

        # ================================================
        # CÓ KẾT QUẢ
        # ================================================

        return {
            "found": True,
            "ingredient_name": ingredient_name,
            "status": status,
            "count": len(results),
            "data": results,
        }

    return get_stock_tool

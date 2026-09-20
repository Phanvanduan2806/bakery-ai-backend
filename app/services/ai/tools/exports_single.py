from app.services.kho.exports_single import get_single_exports


def create_exports_single_tool(
    authorization: str,
):
    def get_exports_single_tool(
        ingredient_name: str = "",
        from_date: str = "",
        to_date: str = "",
        limit: int = 20,
    ) -> dict:
        """
        Lấy và tìm lịch sử xuất kho lẻ.

        Tool này chỉ đọc dữ liệu.
        Không tạo phiếu.
        Không thay đổi tồn kho.
        """

        try:
            result = get_single_exports(
                authorization=authorization,
                ingredient_name=ingredient_name,
                from_date=from_date,
                to_date=to_date,
                limit=limit,
            )

            if not result:
                return {
                    "success": False,
                    "found": False,
                    "ingredient_name": ingredient_name,
                    "from_date": from_date,
                    "to_date": to_date,
                    "message": (
                        f"Không tìm thấy lịch sử xuất kho "
                        f"của '{ingredient_name}'."
                        if ingredient_name
                        else "Không có dữ liệu lịch sử xuất kho."
                    ),
                }

            return {
                "success": True,
                "found": True,
                "ingredient_name": ingredient_name,
                "from_date": from_date,
                "to_date": to_date,
                "count": len(result),
                "data": result,
            }

        except Exception as error:
            return {
                "success": False,
                "message": str(error),
            }

    return get_exports_single_tool

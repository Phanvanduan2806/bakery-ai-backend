from app.services.kho.imports import get_imports


def create_imports_tool(authorization: str):

    def get_imports_tool(
        ingredient_name: str = "",
        from_date: str = "",
        to_date: str = "",
        limit: int = 20,
    ) -> dict:

        try:

            results = get_imports(
                authorization=authorization,
                ingredient_name=ingredient_name,
                from_date=from_date,
                to_date=to_date,
                limit=limit,
            )

            if not results:
                return {
                    "found": False,
                    "ingredient_name": ingredient_name,
                    "from_date": from_date,
                    "to_date": to_date,
                    "message": (
                        f"Không tìm thấy lịch sử nhập kho "
                        f"của '{ingredient_name}'."
                        if ingredient_name
                        else "Không có dữ liệu lịch sử nhập kho."
                    ),
                }

            return {
                "found": True,
                "ingredient_name": ingredient_name,
                "from_date": from_date,
                "to_date": to_date,
                "count": len(results),
                "data": results,
            }

        except Exception as error:

            return {
                "found": False,
                "message": str(error),
            }

    return get_imports_tool
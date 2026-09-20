from app.services.kho import find_ingredient


def create_ingredients_tool(
    authorization: str,
):
    def get_ingredients_tool(
        ingredient_name: str = "",
    ) -> dict:
        """
        Tìm thông tin một nguyên liệu theo tên.

        Không dùng tool này để xác định tồn kho.
        """

        if not ingredient_name.strip():
            return {
                "found": False,
                "message": (
                    "Chưa cung cấp tên nguyên liệu "
                    "cần tìm."
                ),
            }

        results = find_ingredient(
            authorization,
            ingredient_name,
        )

        if not results:
            return {
                "found": False,
                "ingredient_name": ingredient_name,
                "message": (
                    f"Không tìm thấy nguyên liệu "
                    f"'{ingredient_name}'."
                ),
            }

        return {
            "found": True,
            "ingredient_name": ingredient_name,
            "data": results,
        }

    return get_ingredients_tool

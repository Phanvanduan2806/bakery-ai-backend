from app.services.kho.exports_recipe import get_recipe_exports


def create_exports_recipe_tool(authorization: str):

    def get_exports_recipe_tool(
        recipe_name: str = "",
        from_date: str = "",
        to_date: str = "",
        limit: int = 20,
    ) -> dict:

        try:
            results = get_recipe_exports(
                authorization=authorization,
                recipe_name=recipe_name,
                from_date=from_date,
                to_date=to_date,
                limit=limit,
            )

            if not results:
                return {
                    "found": False,
                    "recipe_name": recipe_name,
                    "from_date": from_date,
                    "to_date": to_date,
                    "message": (
                        "Không tìm thấy dữ liệu "
                        "lịch sử xuất kho theo công thức."
                    ),
                }

            return {
                "found": True,
                "recipe_name": recipe_name,
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

    return get_exports_recipe_tool

from app.services.kho.recipes import get_recipes


def create_recipes_tool(authorization: str):

    def get_recipes_tool() -> dict:

        try:

            results = get_recipes(
                authorization
            )

            if not results:
                return {
                    "found": False,
                    "message": "Không có dữ liệu công thức bánh."
                }

            return {
                "found": True,
                "count": len(results),
                "data": results,
            }

        except Exception as error:

            return {
                "found": False,
                "message": str(error),
            }

    return get_recipes_tool
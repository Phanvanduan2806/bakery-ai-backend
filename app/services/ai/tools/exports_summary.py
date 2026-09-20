from app.services.kho.exports_summary import get_exports_summary


def create_exports_summary_tool(authorization: str):

    def get_exports_summary_tool(
        from_date: str = "",
        to_date: str = "",
    ) -> dict:

        try:

            result = get_exports_summary(
                authorization=authorization,
                from_date=from_date,
                to_date=to_date,
            )

            return {
                "success": True,
                "from_date": from_date,
                "to_date": to_date,
                "single_total": result["single_total"],
                "recipe_total": result["recipe_total"],
                "total": result["total"],
                "single_count": result["single_count"],
                "recipe_count": result["recipe_count"],
            }

        except Exception as error:

            return {
                "success": False,
                "message": str(error),
            }

    return get_exports_summary_tool
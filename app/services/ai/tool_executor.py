import json


def execute_tool(
    tool_name: str,
    arguments: dict,
    get_ingredients_tool,
    get_stock_tool,
    create_exports_single_tool,
    create_exports_recipe_tool,
):
    if tool_name == "get_ingredients_tool":
        return get_ingredients_tool(
            **arguments
        )

    if tool_name == "get_stock_tool":
        return get_stock_tool(
            **arguments
        )

    if tool_name == "create_exports_single_tool":
        return create_exports_single_tool(
            **arguments
        )
    if tool_name == "create_exports_recipe_tool":
            return create_exports_recipe_tool(
                **arguments
            )
    return {
        "error": f"Unknown tool: {tool_name}"
    }


def serialize_tool_result(result) -> str:
    return json.dumps(
        result,
        ensure_ascii=False,
    )

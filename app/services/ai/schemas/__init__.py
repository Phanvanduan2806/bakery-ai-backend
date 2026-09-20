from app.services.ai.schemas.ingredients import (
    INGREDIENTS_TOOL_SCHEMA,
)

from app.services.ai.schemas.stock import (
    STOCK_TOOL_SCHEMA,
)
from app.services.ai.schemas.exports_single import (
    EXPORTS_SINGLE_TOOL_SCHEMA,
)
from app.services.ai.schemas.exports_recipe import (
    EXPORTS_RECIPE_TOOL_SCHEMA,
)
from app.services.ai.schemas.exports_summary import (
    EXPORTS_SUMMARY_TOOL_SCHEMA,
)
from app.services.ai.schemas.recipes import (
    RECIPES_TOOL_SCHEMA,
)
from app.services.ai.schemas.imports import (
    IMPORTS_TOOL_SCHEMA,
)

TOOLS_SCHEMA = [
    INGREDIENTS_TOOL_SCHEMA,
    STOCK_TOOL_SCHEMA,
    EXPORTS_SINGLE_TOOL_SCHEMA,
    EXPORTS_RECIPE_TOOL_SCHEMA,
    EXPORTS_SUMMARY_TOOL_SCHEMA,
    RECIPES_TOOL_SCHEMA,
    IMPORTS_TOOL_SCHEMA
]

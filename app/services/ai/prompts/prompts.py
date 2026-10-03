from app.services.ai.prompts.scope import SCOPE_PROMPT
from app.services.ai.prompts.data_rules import DATA_RULES_PROMPT
from app.services.ai.prompts.response import RESPONSE_PROMPT
from app.services.ai.prompts.grounding import GROUNDING_PROMPT

SYSTEM_INSTRUCTION = f"""
Bạn là Bakery AI Assistant.

{SCOPE_PROMPT}

{DATA_RULES_PROMPT}

{RESPONSE_PROMPT}

{GROUNDING_PROMPT}
"""

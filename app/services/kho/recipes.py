import os

import requests
from dotenv import load_dotenv

load_dotenv()

WAREHOUSE_API_URL = os.getenv(
    "WAREHOUSE_API_URL"
)


# =========================================================
# GET ALL RECIPES
# =========================================================

def get_recipes(
    authorization: str,
):
    response = requests.get(
        f"{WAREHOUSE_API_URL}/recipes",
        headers={
            "Authorization": authorization,
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    if isinstance(data, dict):
        return data.get("data", data)

    return data
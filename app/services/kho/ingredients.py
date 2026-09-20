import os

import requests
from dotenv import load_dotenv

load_dotenv()

WAREHOUSE_API_URL = os.getenv("WAREHOUSE_API_URL")


# =========================================================
# LẤY DANH SÁCH NGUYÊN LIỆU
# =========================================================

def get_ingredients(
    authorization: str,
):
    response = requests.get(
        f"{WAREHOUSE_API_URL}/ingredients",
        headers={
            "Authorization": authorization,
        },
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# TÌM NGUYÊN LIỆU
# =========================================================

def find_ingredient(
    authorization: str,
    ingredient_name: str,
):
    ingredients = get_ingredients(
        authorization
    )

    keyword = ingredient_name.strip().lower()

    results = []

    for ingredient in ingredients:

        name = str(
            ingredient.get("name")
            or ingredient.get("ten")
            or ingredient.get("title")
            or ""
        ).strip().lower()

        if keyword in name:
            results.append(ingredient)

    return results

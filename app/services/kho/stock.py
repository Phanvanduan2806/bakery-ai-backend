import os

import requests
from dotenv import load_dotenv

load_dotenv()

WAREHOUSE_API_URL = os.getenv("WAREHOUSE_API_URL")


# =========================================================
# LẤY TỒN KHO
# =========================================================

def get_stock(
    authorization: str,
):
    response = requests.get(
        f"{WAREHOUSE_API_URL}/stock",
        headers={
            "Authorization": authorization,
        },
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


# =========================================================
# TÌM / LỌC TỒN KHO
# =========================================================

def find_stock(
    authorization: str,
    ingredient_name: str = "",
    status: str = "",
):
    stock = get_stock(
        authorization
    )

    keyword = ingredient_name.strip().lower()
    status = status.strip().lower()

    results = []

    for item in stock:

        name = str(
            item.get("name")
            or item.get("ten")
            or item.get("ingredient_name")
            or item.get("title")
            or ""
        ).strip()

        name_lower = name.lower()

        # =================================================
        # 1. LỌC THEO TÊN
        # =================================================

        if keyword and keyword not in name_lower:
            continue

        # =================================================
        # 2. LẤY SỐ LƯỢNG
        # =================================================

        try:
            quantity = float(
                item.get("quantity") or 0
            )
        except (TypeError, ValueError):
            quantity = 0

        # =================================================
        # 3. LỌC THEO TRẠNG THÁI
        # =================================================

        if status == "out":
            if quantity > 0:
                continue

        elif status == "low":
            if quantity <= 0 or quantity >= 1000:
                continue

        # =================================================
        # 4. THÊM VÀO KẾT QUẢ
        # =================================================

        results.append(item)

    return results

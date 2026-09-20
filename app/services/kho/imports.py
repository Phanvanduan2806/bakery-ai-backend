import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

load_dotenv()

WAREHOUSE_API_URL = os.getenv(
    "WAREHOUSE_API_URL"
)


def get_imports(
    authorization: str,
    ingredient_name: str = "",
    from_date: str = "",
    to_date: str = "",
    limit: int = 20,
):
    response = requests.get(
        f"{WAREHOUSE_API_URL}/imports",
        headers={
            "Authorization": authorization,
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    if isinstance(data, dict):
        data = data.get("data", [])


    # =====================================================
    # LỌC THEO TÊN NGUYÊN LIỆU
    # =====================================================

    if ingredient_name.strip():

        keyword = ingredient_name.strip().lower()

        data = [
            item
            for item in data
            if keyword in item.get(
                "ingredient_name",
                ""
            ).lower()
        ]


    # =====================================================
    # LỌC TỪ NGÀY
    # =====================================================

    if from_date:

        from_datetime = datetime.strptime(
            from_date,
            "%Y-%m-%d",
        )

        data = [
            item
            for item in data
            if datetime.strptime(
                item.get("created_at", ""),
                "%Y-%m-%d %H:%M:%S",
            ) >= from_datetime
        ]


    # =====================================================
    # LỌC ĐẾN NGÀY
    # =====================================================

    if to_date:

        to_datetime = datetime.strptime(
            to_date,
            "%Y-%m-%d",
        )

        end_datetime = (
            to_datetime + timedelta(days=1)
        )

        data = [
            item
            for item in data
            if datetime.strptime(
                item.get("created_at", ""),
                "%Y-%m-%d %H:%M:%S",
            ) < end_datetime
        ]


    # =====================================================
    # SẮP XẾP MỚI NHẤT
    # =====================================================

    data.sort(
        key=lambda item: item.get(
            "created_at",
            ""
        ),
        reverse=True,
    )


    # =====================================================
    # GIỚI HẠN KẾT QUẢ
    # =====================================================

    if from_date or to_date:
        return data

    return data[:limit]
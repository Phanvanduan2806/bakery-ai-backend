import os

import requests
from dotenv import load_dotenv

load_dotenv()

WAREHOUSE_API_URL = os.getenv("WAREHOUSE_API_URL")


# =========================================================
# LẤY THÔNG TIN USER HIỆN TẠI
# =========================================================

def get_current_user(
    authorization: str,
):
    response = requests.get(
        f"{WAREHOUSE_API_URL}/me",
        headers={
            "Authorization": authorization,
        },
        timeout=10,
    )

    response.raise_for_status()

    return response.json()

from app.services.kho.exports_single import get_single_exports
from app.services.kho.exports_recipe import get_recipe_exports


def get_exports_summary(
    authorization: str,
    from_date: str = "",
    to_date: str = "",
):
    # =====================================================
    # 1. LẤY XUẤT KHO LẺ
    # =====================================================

    single_exports = get_single_exports(
        authorization=authorization,
        from_date=from_date,
        to_date=to_date,
        limit=999999,
    )

    # =====================================================
    # 2. TÍNH TIỀN XUẤT LẺ
    # =====================================================

    single_total = 0

    for item in single_exports:

        quantity = float(
            item.get("quantity", 0)
        )

        base_price = float(
            item.get("base_price", 0)
        )

        single_total += (
            quantity * base_price
        )

    # =====================================================
    # 3. LẤY XUẤT KHO THEO CÔNG THỨC
    # =====================================================

    recipe_exports = get_recipe_exports(
        authorization=authorization,
        from_date=from_date,
        to_date=to_date,
        limit=999999,
    )

    # =====================================================
    # 4. TÍNH TIỀN XUẤT CÔNG THỨC
    # =====================================================

    recipe_total = 0

    for item in recipe_exports:

        quantity = float(
            item.get("quantity", 0)
        )

        total_price = float(
            item.get("total_price", 0)
        )

        recipe_total += (
            quantity * total_price
        )

    # =====================================================
    # 5. TỔNG TIỀN NGUYÊN LIỆU
    # =====================================================

    total = single_total + recipe_total

    return {
        "from_date": from_date,
        "to_date": to_date,

        "single_total": single_total,

        "recipe_total": recipe_total,

        "total": total,

        "single_count": len(single_exports),

        "recipe_count": len(recipe_exports),
    }
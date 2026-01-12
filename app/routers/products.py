from fastapi import APIRouter, Query
from app.supabase_client import get_products, get_product_by_id

router = APIRouter(tags=["Products"])

@router.get("/products/")
def list_products(
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    search: str | None = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: str = "name",
    order: str = "asc"
):
    return get_products(
        category=category,
        min_price=min_price,
        max_price=max_price,
        search=search,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        order=order
    )

@router.get("/products/{product_id}/")
def product_detail(product_id: int):
    return get_product_by_id(product_id)
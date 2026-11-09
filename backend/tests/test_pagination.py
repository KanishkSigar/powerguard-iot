"""
PowerGuard IoT — Pagination Unit Tests
Validates pagination utility for telemetry and alert query lists.
"""
from typing import List, Dict, Any
import pytest


def paginate(items: List[Any], page: int = 1, page_size: int = 10) -> Dict[str, Any]:
    """Slices an in-memory list into pagination metadata and items."""
    total = len(items)
    page_size = max(1, page_size)
    total_pages = max(1, (total + page_size - 1) // page_size)
    page = max(1, min(page, total_pages)) if total > 0 else 1
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "items": items[start:end],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }


def test_pagination_first_page():
    data = list(range(100))
    res = paginate(data, page=1, page_size=20)
    assert res["total"] == 100
    assert res["page"] == 1
    assert res["total_pages"] == 5
    assert len(res["items"]) == 20
    assert res["items"][0] == 0
    assert res["items"][-1] == 19
    assert res["has_next"] is True
    assert res["has_prev"] is False


def test_pagination_middle_page():
    data = list(range(100))
    res = paginate(data, page=3, page_size=20)
    assert res["page"] == 3
    assert res["items"][0] == 40
    assert res["has_next"] is True
    assert res["has_prev"] is True


def test_pagination_last_page():
    data = list(range(45))
    res = paginate(data, page=5, page_size=10)
    assert res["page"] == 5
    assert res["total_pages"] == 5
    assert len(res["items"]) == 5
    assert res["has_next"] is False
    assert res["has_prev"] is True


def test_pagination_empty():
    res = paginate([], page=1, page_size=10)
    assert res["total"] == 0
    assert res["items"] == []
    assert res["has_next"] is False
    assert res["has_prev"] is False
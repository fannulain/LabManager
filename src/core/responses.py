"""
Standardized REST API Response Formatter Component.
Ensures consistent pagination and JSON structures across all endpoints.
"""

from typing import Any, Sequence

def paginated_response(items: Sequence[Any], total: int = None) -> dict:
    """Format paginated collection payload."""
    return {
        "items": list(items),
        "total": len(items) if total is None else total
    }

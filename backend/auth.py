from fastapi import HTTPException, Request
from functools import wraps
from backend.tiers import get_tier

TIER_ORDER = ["Free", "Basic", "Pro", "Enterprise"]

def require_tier(minimum_tier: str):
    """
    Decorator restricting endpoints to a minimum tier.
    Example:
        @app.get("/pro-feature/{username}")
        @require_tier("Pro")
        async def pro_feature(username: str):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

            username = kwargs.get("username")
            if not username and request:
                username = request.headers.get("X-User")

            # --> handle missing username (return 403 instead of crash)
            if not username:
                raise HTTPException(
                    status_code=403,
                    detail="Forbidden: username missing or invalid."
                )

            user_tier = get_tier(username)
            if TIER_ORDER.index(user_tier) < TIER_ORDER.index(minimum_tier):
                raise HTTPException(
                    status_code=403,
                    detail=f"{minimum_tier}+ required (current: {user_tier})"
                )

            return await func(*args, **kwargs)

        return wrapper
    return decorator
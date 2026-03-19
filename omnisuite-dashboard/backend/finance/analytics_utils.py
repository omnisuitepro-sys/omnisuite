# ------------------------------------------------------------
# Finance Analytics Utilities
# ------------------------------------------------------------
from sqlalchemy import func
from backend.finance import models

# ------------------------------------------------------------
# Cash Velocity Analyzer
# ------------------------------------------------------------
def check_cash_velocity(user_id, db):
    """
    Determine user's short-term liquidity (Cash Velocity)
    = bank balance - total unpaid bills.
    """
    # Step 1: collect balances (replace with Plaid call)
    from backend.finance.plaid_utils import get_total_balance
    try:
        balance = get_total_balance(user_id)
    except Exception:
        balance = 0.0

    # Step 2: sum unpaid bills
    total_bills = (
        db.query(func.sum(models.BillTracker.amount))
          .filter_by(user_id=user_id, status="unpaid")
          .scalar()
        or 0.0
    )

    # Step 3: calculate velocity
    velocity = balance - total_bills

    if velocity < 500:
        return {
            "status": "critical",
            "message": "⚠️ Low cash velocity — postpone non‑essential spend",
            "balance": balance,
            "upcoming_bills": total_bills,
            "available_after_bills": velocity
        }
    return {
        "status": "healthy",
        "message": f"✅ ${round(velocity,2)} available after bills",
        "balance": balance,
        "upcoming_bills": total_bills,
        "available_after_bills": velocity
    }
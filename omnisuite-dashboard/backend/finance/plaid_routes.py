from fastapi import APIRouter, Depends
from backend.finance.plaid_utils import save_subscriptions_to_db
from backend.db_session import get_session

router = APIRouter(prefix="/api/v1/plaid", tags=["Plaid"])

@router.post("/scan/{user_id}")
def scan_bank_subscriptions(user_id: str, db=Depends(get_session)):
    """Fetch latest 30‑day recurring subscriptions via Plaid."""
    user_link = db.query(models.UserBankLink).filter_by(user_id=user_id).first()
    if not user_link:
        return {"error": "No bank link available for user"}
    subs = save_subscriptions_to_db(user_id, user_link.plaid_access_token)
    return {"found": len(subs), "subscriptions": subs}
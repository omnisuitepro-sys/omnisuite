# ------------------------------------------------------------
# Omni Alpha Financial API
# ------------------------------------------------------------
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db_session import get_session as get_db
from backend.crud import log_event
from backend.finance import plaid_utils, analytics_utils
from backend.finance.plaid_routes import router as plaid_router
from backend.finance.bill_tracker import router as bill_router

# Create a sub‑app that will be mounted under /alpha in main.py
app = FastAPI(title="Omni Alpha Financial API", version="1.0.0")

# -------------------------- STATUS CHECK ---------------------------
@app.get("/status")
def status():
    """Confirm the Finance sub‑application is active."""
    return {
        "status": "ok",
        "module": "Omni Alpha Financial",
        "message": "Finance routes successfully imported"
    }

# --------------------- SUBSCRIPTIONS & METRICS ---------------------
@app.get("/subscriptions/{user_id}")
def scan_subscriptions(user_id: str, db: Session = Depends(get_db)):
    """Fetch 30‑day transactions and flag recurring subscriptions."""
    try:
        user_link = db.execute(
            "SELECT plaid_access_token FROM bank_links WHERE user_id = :uid",
            {"uid": user_id}
        ).fetchone()
        if not user_link:
            raise HTTPException(status_code=404, detail="No Plaid bank link found.")

        subs = plaid_utils.get_monthly_subscriptions(user_link[0])
        log_event("INFO", f"{len(subs)} subscriptions pulled for {user_id}", "plaid")
        return {"user_id": user_id, "subscriptions": subs}

    except Exception as e:
        log_event("ERROR", f"Subscription scan failed for {user_id}: {e}", "plaid")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/cash-velocity/{user_id}")
def check_velocity(user_id: str, db: Session = Depends(get_db)):
    """Analyze current liquidity versus upcoming bills."""
    try:
        result = analytics_utils.check_cash_velocity(user_id, db)
        log_event("INFO", f"Cash velocity checked for {user_id}", "analytics")
        return result
    except Exception as e:
        log_event("ERROR", f"Cash velocity error for {user_id}: {e}", "analytics")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))

# -------------------------- ROUTER REGISTRATION --------------------
# Attach existing routers from Plaid and Bill Tracker
app.include_router(plaid_router)
app.include_router(bill_router)
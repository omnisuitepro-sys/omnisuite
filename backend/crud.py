# crud.py
from datetime import datetime
from backend.db_session import get_session
from backend.db_init import License, PendingTrade, SystemLog

# ---------- LICENSES ----------
def add_license(username: str, tier: str, expiry: datetime):
    with get_session() as db:
        record = db.query(License).filter_by(username=username).first()
        if record:
            record.tier = tier
            record.expiry = expiry
        else:
            db.add(License(username=username, tier=tier, expiry=expiry))
        return {"username": username, "tier": tier, "expiry": expiry.isoformat()}

def get_license(username: str):
    with get_session() as db:
        record = db.query(License).filter_by(username=username).first()
        if record:
            return {
                "username": record.username,
                "tier": record.tier,
                "expiry": record.expiry,
            }
        return None

# ---------- PENDING TRADES ----------
def add_pending_trade(trade_id, symbol, side, reason):
    with get_session() as db:
        db.add(PendingTrade(
            trade_id=trade_id,
            symbol=symbol,
            side=side,
            reason=reason,
            created_at=datetime.utcnow()
        ))
        return {"trade_id": trade_id, "symbol": symbol, "side": side}

def get_pending_trades():
    with get_session() as db:
        trades = db.query(PendingTrade).all()
        return [{
            "trade_id": t.trade_id,
            "symbol": t.symbol,
            "side": t.side,
            "reason": t.reason,
            "status": t.status,
            "created_at": t.created_at.isoformat()
        } for t in trades]

def approve_trade(trade_id):
    with get_session() as db:
        trade = db.query(PendingTrade).filter_by(trade_id=trade_id).first()
        if trade:
            trade.status = "executed"
            return {"trade_id": trade_id, "status": "executed"}
        return {"error": "Trade not found"}

# ---------- LOGGING ----------
def log_event(level: str, message: str, source: str = "core"):
    with get_session() as db:
        db.add(SystemLog(level=level, message=message, source=source))
        return {"logged": True, "level": level, "source": source}
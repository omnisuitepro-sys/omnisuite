# ------------------------------------------------------------
# bill_tracker.py  —  OmniSuite Finance Bill Tracking API
# ------------------------------------------------------------
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from backend.db_session import get_session as get_db
from backend.finance import models

# Declare the router so omni_alpha_routes.py can import it
router = APIRouter(prefix="/api/v1/bills", tags=["Bill Tracker"])


# ------------------------------------------------------------
# Create Bill
# ------------------------------------------------------------
@router.post("/create")
def create_bill(
    user_id: str,
    vendor: str,
    amount: float,
    due_date: str,
    db: Session = Depends(get_db)
):
    """Add a new bill record for a user."""
    try:
        new_bill = models.BillTracker(
            user_id=user_id,
            vendor=vendor,
            amount=amount,
            due_date=datetime.strptime(due_date, "%Y-%m-%d"),
            status="unpaid",
        )
        db.add(new_bill)
        db.commit()
        return {"status": "success", "message": f"Bill for {vendor} added."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------------
# List Bills by User
# ------------------------------------------------------------
@router.get("/{user_id}")
def list_bills(user_id: str, db: Session = Depends(get_db)):
    """Return bills (paid + unpaid) for a specific user."""
    bills = db.query(models.BillTracker).filter_by(user_id=user_id).all()
    return {"user_id": user_id, "total": len(bills), "bills": bills}


# ------------------------------------------------------------
# Mark Bill as Paid
# ------------------------------------------------------------
@router.put("/mark-paid/{bill_id}")
def mark_bill_paid(bill_id: int, db: Session = Depends(get_db)):
    """Mark a bill as paid."""
    bill = db.query(models.BillTracker).filter_by(id=bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found.")
    bill.status = "paid"
    db.commit()
    return {"status": "success", "message": f"Bill ID {bill_id} marked as paid."}


# ------------------------------------------------------------
# Delete Bill
# ------------------------------------------------------------
@router.delete("/delete/{bill_id}")
def delete_bill(bill_id: int, db: Session = Depends(get_db)):
    """Delete a bill record."""
    bill = db.query(models.BillTracker).filter_by(id=bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found.")
    db.delete(bill)
    db.commit()
    db.refresh(new_bill)
    return {"status": "success", "message": f"Bill ID {bill_id} deleted."}
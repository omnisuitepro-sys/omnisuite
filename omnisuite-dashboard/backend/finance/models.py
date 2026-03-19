# ------------------------------------------------------------
# Omni Financial: Banking & Bill Tracking Models
# ------------------------------------------------------------
from sqlalchemy import Column, Integer, String, Float, DateTime
from backend.core.db_base import Base
import datetime

class UserBankLink(Base):
    __tablename__ = "bank_links"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    plaid_access_token = Column(String)       # (Store encrypted token)
    institution_name = Column(String)

    def __repr__(self):
        return f"<UserBankLink user_id={self.user_id}, institution={self.institution_name}>"

class BillTracker(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    vendor = Column(String)
    amount = Column(Float)
    due_date = Column(DateTime)
    status = Column(String, default="unpaid")   # unpaid | paid | pending | late
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<BillTracker user_id={self.user_id}, vendor={self.vendor}, amount={self.amount}>"
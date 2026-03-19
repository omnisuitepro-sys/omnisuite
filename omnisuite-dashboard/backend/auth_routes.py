# ------------------------------------------------------------
# Authentication Routes
# ------------------------------------------------------------
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db_session import get_session as get_db
from backend.models_user import User
from backend.auth_utils import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/register")
def register_user(email: str, password: str, db: Session = Depends(get_db)):
    """Create a new user account."""
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(email=email, hashed_password=hash_password(password))
    db.add(new_user)
    db.commit()
    return {"status": "success", "message": f"Account created for {email}"}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    """Authenticate and issue a JWT token."""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
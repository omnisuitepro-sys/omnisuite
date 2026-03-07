# ------------------------------------------------------------
# main.py — OmniSuite Backend Entry Point
# ------------------------------------------------------------
import os
print("🚀 CURRENT DB_URL =", os.getenv("DB_URL"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI app FIRST (avoids NameError)
app = FastAPI(title="OmniSuite Backend", version="1.0.0")

# ------------------------------------------------------------
# Global Middleware (CORS, etc.)
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# Mount Finance Module (/alpha)
# ------------------------------------------------------------
from backend.finance.omni_alpha_routes import app as alpha_finance_app
app.mount("/alpha", alpha_finance_app)

# ------------------------------------------------------------
# Root endpoint
# ------------------------------------------------------------
@app.get("/")
def root():
    return {"service": "OmniSuite Backend", "status": "online"}
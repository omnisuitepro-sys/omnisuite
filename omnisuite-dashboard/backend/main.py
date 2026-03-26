print("✅ NEW BACKEND FILE LOADED")

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS (frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# ROOT
# ------------------------------------------------------------
@app.get("/")
def root():
    return {"status": "ok", "service": "OmniSuite Backend"}

# ------------------------------------------------------------
# LISTINGS (GET)
# ------------------------------------------------------------
@app.get("/listings")
def get_listings():
    return [
        {"id": 1, "title": "Test Product", "price": 10.0}
    ]

# ------------------------------------------------------------
# LISTINGS (POST) ✅ FIXES 405
# ------------------------------------------------------------
@app.post("/listings")
def create_listing(data: dict = Body(...)):
    return {
        "status": "created",
        "item": data
    }

# ------------------------------------------------------------
# TABS (GET)
# ------------------------------------------------------------
@app.get("/tabs")
def get_tabs():
    return [
        {"id": 1, "name": "General"},
        {"id": 2, "name": "Amazon"},
        {"id": 3, "name": "eBay"},
    ]

# ------------------------------------------------------------
# TABS (POST)
# ------------------------------------------------------------
@app.post("/tabs")
def create_tab(data: dict = Body(...)):
    return {
        "status": "created",
        "tab": data
    }

# ------------------------------------------------------------
# METRICS
# ------------------------------------------------------------
@app.get("/metrics")
def get_metrics():
    return {
        "total_listings": 1,
        "total_value": 10.0,
        "avg_price": 10.0
    }
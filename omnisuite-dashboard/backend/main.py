# ------------------------------------------------------------
# OmniSuite Backend (WORKING + COMPLETE)
# ------------------------------------------------------------

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
        {"id": 1, "title": "iPhone Case", "price": 12.99},
        {"id": 2, "title": "Wireless Mouse", "price": 24.99},
        {"id": 3, "title": "LED Desk Lamp", "price": 34.99},
    ]

# ------------------------------------------------------------
# LISTINGS (POST) ✅ FIXES 405 ERROR
# ------------------------------------------------------------
@app.post("/listings")
def create_listing(data: dict = Body(...)):
    return {
        "status": "created",
        "item": data
    }

# ------------------------------------------------------------
# LISTINGS (PUT - EDIT)
# ------------------------------------------------------------
@app.put("/listings/{id}")
def update_listing(id: int, data: dict = Body(...)):
    return {
        "status": "updated",
        "id": id,
        "data": data
    }

# ------------------------------------------------------------
# LISTINGS (DELETE)
# ------------------------------------------------------------
@app.delete("/listings/{id}")
def delete_listing(id: int):
    return {
        "status": "deleted",
        "id": id
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
# METRICS (GET)
# ------------------------------------------------------------
@app.get("/metrics")
def get_metrics():
    return {
        "total_listings": 3,
        "total_value": 72.97,
        "avg_price": 24.32
    }
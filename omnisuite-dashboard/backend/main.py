# ------------------------------------------------------------
# main.py — OmniSuite Backend Entry Point
# ------------------------------------------------------------

import os
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

print("🚀 CURRENT DB_URL =", os.getenv("DB_URL"))

# ------------------------------------------------------------
# Initialize FastAPI
# ------------------------------------------------------------
app = FastAPI(title="OmniSuite Backend", version="1.0.0")

# ------------------------------------------------------------
# CORS (allow frontend access)
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# Database connection helper
# ------------------------------------------------------------
DB_URL = os.getenv("DB_URL")

def get_db():
    return psycopg2.connect(DB_URL)

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
    return {"service": "OmniSuite Backend", "status": "online"}


# ------------------------------------------------------------
# GET Listings (from database)
# ------------------------------------------------------------
@app.get("/listings")
def get_listings():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, title, price FROM listings ORDER BY id DESC;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {"id": r[0], "title": r[1], "price": float(r[2])}
        for r in rows
    ]


# ------------------------------------------------------------
# CREATE Listing (save to database)
# ------------------------------------------------------------
@app.post("/listings")
def create_listing(data: dict = Body(...)):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO listings (title, price) VALUES (%s, %s) RETURNING id;",
        (data["title"], data["price"]),
    )

    new_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return {"id": new_id, "status": "created"}

# ------------------------------------------------------------
# UPDATE Listing
# ------------------------------------------------------------
@app.put("/listings/{id}")
def update_listing(id: int, data: dict):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE listings SET title=%s, price=%s WHERE id=%s;",
        (data["title"], data["price"], id),
    )

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "updated"}


# ------------------------------------------------------------
# DELETE Listing
# ------------------------------------------------------------
@app.delete("/listings/{id}")
def delete_listing(id: int):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM listings WHERE id=%s;", (id,))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "deleted"}
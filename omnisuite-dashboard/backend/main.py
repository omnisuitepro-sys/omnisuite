# ------------------------------------------------------------
# main.py — OmniSuite Backend (FULL VERSION)
# ------------------------------------------------------------

import os
import psycopg2
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# ------------------------------------------------------------
# Init App
# ------------------------------------------------------------
app = FastAPI(title="OmniSuite Backend", version="1.0.0")

# ------------------------------------------------------------
# CORS (allow frontend)
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# Database Connection (Neon)
# ------------------------------------------------------------
DB_URL = os.getenv("DB_URL")

if not DB_URL:
    print("❌ DB_URL is NOT set")
else:
    print("✅ DB_URL loaded")

def get_db():
    try:
        return psycopg2.connect(DB_URL)
    except Exception as e:
        print("DB CONNECTION ERROR:", e)
        raise HTTPException(status_code=500, detail="Database connection failed")

# ------------------------------------------------------------
# Mount Finance Module (/alpha)
# ------------------------------------------------------------
from backend.finance.omni_alpha_routes import app as alpha_finance_app
app.mount("/alpha", alpha_finance_app)

# ------------------------------------------------------------
# Root
# ------------------------------------------------------------
@app.get("/")
def root():
    return {"service": "OmniSuite Backend", "status": "online"}

# ------------------------------------------------------------
# GET ALL LISTINGS
# ------------------------------------------------------------
@app.get("/listings")
def get_listings():
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, title, price FROM listings ORDER BY id DESC;")
        rows = cur.fetchall()

        return [
            {"id": r[0], "title": r[1], "price": float(r[2])}
            for r in rows
        ]

    except Exception as e:
        print("GET ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch listings")

    finally:
        cur.close()
        conn.close()

# ------------------------------------------------------------
# CREATE LISTING
# ------------------------------------------------------------
@app.post("/listings")
def create_listing(data: dict = Body(...)):
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO listings (title, price) VALUES (%s, %s) RETURNING id;",
            (data["title"], data["price"]),
        )

        new_id = cur.fetchone()[0]
        conn.commit()

        return {"id": new_id, "status": "created"}

    except Exception as e:
        print("CREATE ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to create listing")

    finally:
        cur.close()
        conn.close()

# ------------------------------------------------------------
# UPDATE LISTING
# ------------------------------------------------------------
@app.put("/listings/{id}")
def update_listing(id: int, data: dict = Body(...)):
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "UPDATE listings SET title=%s, price=%s WHERE id=%s;",
            (data["title"], data["price"], id),
        )

        conn.commit()

        return {"status": "updated"}

    except Exception as e:
        print("UPDATE ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to update listing")

    finally:
        cur.close()
        conn.close()

# ------------------------------------------------------------
# DELETE LISTING
# ------------------------------------------------------------
@app.delete("/listings/{id}")
def delete_listing(id: int):
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM listings WHERE id=%s;", (id,))
        conn.commit()

        return {"status": "deleted"}

    except Exception as e:
        print("DELETE ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to delete listing")

    finally:
        cur.close()
        conn.close()
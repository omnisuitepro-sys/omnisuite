# ------------------------------------------------------------
# OmniSuite Backend (FULL FINAL VERSION)
# ------------------------------------------------------------

import os
import psycopg2
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="OmniSuite Backend", version="1.0.0")

# ------------------------------------------------------------
# CORS
# ------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------
# DB CONNECTION (Neon)
# ------------------------------------------------------------
DB_URL = os.getenv("DB_URL")

def get_db():
    try:
        return psycopg2.connect(DB_URL)
    except Exception as e:
        print("DB ERROR:", e)
        raise HTTPException(status_code=500, detail="DB connection failed")

# ------------------------------------------------------------
# ROOT
# ------------------------------------------------------------
@app.get("/")
def root():
    return {"status": "ok"}

# ------------------------------------------------------------
# METRICS
# ------------------------------------------------------------
@app.get("/metrics")
def get_metrics():
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("SELECT COUNT(*), COALESCE(SUM(price), 0), COALESCE(AVG(price), 0) FROM listings;")
        result = cur.fetchone()

        return {
            "total_listings": result[0],
            "total_value": float(result[1]),
            "avg_price": float(result[2])
        }

    except Exception as e:
        print("METRICS ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch metrics")

    finally:
        cur.close()
        conn.close()

# ------------------------------------------------------------
# TABS
# ------------------------------------------------------------
@app.get("/tabs")
def get_tabs():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM tabs ORDER BY id ASC;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [{"id": r[0], "name": r[1]} for r in rows]


@app.post("/tabs")
def create_tab(data: dict = Body(...)):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tabs (name) VALUES (%s) RETURNING id;",
        (data["name"],)
    )

    tab_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return {"id": tab_id, "name": data["name"]}

# ------------------------------------------------------------
# LISTINGS
# ------------------------------------------------------------
@app.get("/listings")
def get_listings(tab_id: int = None):
    conn = get_db()
    cur = conn.cursor()

    if tab_id:
        cur.execute(
            "SELECT id, title, price FROM listings WHERE tab_id=%s ORDER BY id DESC;",
            (tab_id,)
        )
    else:
        cur.execute(
            "SELECT id, title, price FROM listings ORDER BY id DESC;"
        )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {"id": r[0], "title": r[1], "price": float(r[2])}
        for r in rows
    ]


@app.post("/listings")
def create_listing(data: dict = Body(...)):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO listings (title, price, tab_id) VALUES (%s, %s, %s) RETURNING id;",
        (data["title"], data["price"], data.get("tab_id"))
    )

    new_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return {"id": new_id}


@app.put("/listings/{id}")
def update_listing(id: int, data: dict = Body(...)):
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


@app.delete("/listings/{id}")
def delete_listing(id: int):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM listings WHERE id=%s;", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return {"status": "deleted"}
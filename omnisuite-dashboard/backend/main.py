import os
import psycopg2
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_URL = os.getenv("DB_URL")

def get_db():
    return psycopg2.connect(DB_URL)

# ---------------- METRICS ----------------
@app.get("/metrics")
def metrics():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
        COUNT(*),
        COALESCE(SUM(price),0),
        COALESCE(AVG(price),0),
        COALESCE(SUM(price - cost),0)
        FROM listings;
    """)

    r = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "total_listings": r[0],
        "total_value": float(r[1]),
        "avg_price": float(r[2]),
        "total_profit": float(r[3])
    }

# ---------------- TABS ----------------
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
def create_tab(data: dict):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO tabs (name) VALUES (%s) RETURNING id;",
        (data["name"],)
    )

    tid = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return {"id": tid, "name": data["name"]}


# ---------------- LISTINGS ----------------
@app.get("/listings")
def get_listings(tab_id: int = None):
    conn = get_db()
    cur = conn.cursor()

    if tab_id:
        cur.execute(
            "SELECT id,title,price FROM listings WHERE tab_id=%s ORDER BY id DESC;",
            (tab_id,)
        )
    else:
        cur.execute(
            "SELECT id,title,price FROM listings ORDER BY id DESC;"
        )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {"id": r[0], "title": r[1], "price": float(r[2])}
        for r in rows
    ]


@app.post("/listings")
def create_listing(data: dict):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO listings (title, price, tab_id) VALUES (%s, %s, %s) RETURNING id;",
        (data["title"], data["price"], data.get("tab_id"))
    )

    nid = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return {"id": nid}
# ---------------- LISTINGS ----------------
@app.get("/listings")
def listings(tab_id: int = None):
    conn = get_db()
    cur = conn.cursor()

    if tab_id:
        cur.execute("SELECT id,title,price,cost FROM listings WHERE tab_id=%s ORDER BY id DESC;", (tab_id,))
    else:
        cur.execute("SELECT id,title,price,cost FROM listings ORDER BY id DESC;")

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": r[0],
            "title": r[1],
            "price": float(r[2]),
            "cost": float(r[3]),
            "profit": float(r[2] - r[3])
        }
        for r in rows
    ]

@app.post("/listings")
def create_listing(data: dict):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO listings (title,price,cost,tab_id) VALUES (%s,%s,%s,%s) RETURNING id;",
        (data["title"], data["price"], data["cost"], data.get("tab_id"))
    )

    nid = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return {"id": nid}

@app.put("/listings/{id}")
def update_listing(id: int, data: dict):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE listings SET title=%s, price=%s, cost=%s WHERE id=%s;",
        (data["title"], data["price"], data["cost"], id)
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
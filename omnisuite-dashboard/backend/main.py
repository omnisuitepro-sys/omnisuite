import os
import psycopg2
import threading
import time
from fastapi import FastAPI, Body
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

def db():
    return psycopg2.connect(DB_URL)

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"status": "ok"}

# ---------------- TABS ----------------
@app.get("/tabs")
def tabs():
    conn=db();cur=conn.cursor()
    cur.execute("SELECT id,name FROM tabs ORDER BY id")
    rows=cur.fetchall()
    cur.close();conn.close()
    return [{"id":r[0],"name":r[1]} for r in rows]

@app.post("/tabs")
def create_tab(data:dict=Body(...)):
    conn=db();cur=conn.cursor()
    cur.execute("INSERT INTO tabs(name) VALUES(%s) RETURNING id;",(data["name"],))
    tid=cur.fetchone()[0]
    conn.commit()
    cur.close();conn.close()
    return {"id":tid}

# ---------------- LISTINGS ----------------
@app.get("/listings")
def listings(tab_id:int=None):
    conn=db();cur=conn.cursor()

    if tab_id:
        cur.execute("SELECT id,title,price,cost FROM listings WHERE tab_id=%s",(tab_id,))
    else:
        cur.execute("SELECT id,title,price,cost FROM listings")

    rows=cur.fetchall()
    cur.close();conn.close()

    return [{
        "id":r[0],
        "title":r[1],
        "price":float(r[2]),
        "cost":float(r[3]),
        "profit":float(r[2]-r[3])
    } for r in rows]

@app.post("/listings")
def create_listing(data:dict=Body(...)):
    conn=db();cur=conn.cursor()
    cur.execute(
        "INSERT INTO listings(title,price,cost,tab_id) VALUES(%s,%s,%s,%s) RETURNING id;",
        (data["title"],data["price"],data.get("cost",0),data.get("tab_id"))
    )
    nid=cur.fetchone()[0]
    conn.commit()
    cur.close();conn.close()
    return {"id":nid}

@app.delete("/listings/{id}")
def delete_listing(id:int):
    conn=db();cur=conn.cursor()
    cur.execute("DELETE FROM listings WHERE id=%s",(id,))
    conn.commit()
    cur.close();conn.close()
    return {"status":"deleted"}

# ---------------- METRICS ----------------
@app.get("/metrics")
def metrics():
    conn=db();cur=conn.cursor()
    cur.execute("""
        SELECT COUNT(*),
        COALESCE(SUM(price),0),
        COALESCE(AVG(price),0),
        COALESCE(SUM(price-cost),0)
        FROM listings
    """)
    r=cur.fetchone()
    cur.close();conn.close()
    return {
        "total_listings":r[0],
        "total_value":float(r[1]),
        "avg_price":float(r[2]),
        "total_profit":float(r[3])
    }

# ---------------- SMART AUTOMATION ----------------
def run_smart():
    conn=db();cur=conn.cursor()

    cur.execute("SELECT COALESCE(AVG(price-cost),0) FROM listings")
    avg_profit=cur.fetchone()[0]

    cur.execute("SELECT id,price,cost FROM listings")
    rows=cur.fetchall()

    for r in rows:
        pid=r[0];price=float(r[1]);cost=float(r[2])
        profit=price-cost

        if profit<avg_profit*0.5:
            cur.execute("DELETE FROM listings WHERE id=%s",(pid,))

        elif profit<avg_profit:
            new_price=round(price*1.08,2)
            cur.execute("UPDATE listings SET price=%s WHERE id=%s",(new_price,pid))

        elif profit>avg_profit*1.5:
            new_price=round(price*1.05,2)
            cur.execute("UPDATE listings SET price=%s WHERE id=%s",(new_price,pid))

    conn.commit()
    cur.close();conn.close()

@app.post("/automation/run")
def automation():
    run_smart()
    return {"status":"done"}

# ---------------- ARBITRAGE ----------------
def find_products():
    return [
        {"title":"Speaker","cost":12,"price":25},
        {"title":"Phone Stand","cost":3,"price":12},
        {"title":"LED Lights","cost":8,"price":22},
    ]

@app.post("/arbitrage/run")
def arbitrage():
    conn=db();cur=conn.cursor()
    products=find_products()

    for p in products:
        if p["price"]-p["cost"]>8:
            cur.execute(
                "INSERT INTO listings(title,price,cost) VALUES(%s,%s,%s)",
                (p["title"],p["price"],p["cost"])
            )

    conn.commit()
    cur.close();conn.close()

    return {"added":len(products)}

# ---------------- AUTO LOOP ----------------
def loop():
    while True:
        try:
            run_smart()
        except Exception as e:
            print(e)
        time.sleep(60)

@app.on_event("startup")
def start():
    t=threading.Thread(target=loop)
    t.daemon=True
    t.start()
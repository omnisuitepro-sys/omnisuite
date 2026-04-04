import os
import base64
import requests
import psycopg2
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

def get_ebay_token():
    import base64

    client_id = os.getenv("EBAY_CLIENT_ID")
    client_secret = os.getenv("EBAY_CLIENT_SECRET")

    auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    r = requests.post("https://api.ebay.com/identity/v1/oauth2/token", headers=headers, data=data)
    return r.json()["access_token"]

def ebay_sold_search(query):
    token = get_ebay_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={query}&filter=soldItems:true&limit=5"

    r = requests.get(url, headers=headers)
    data = r.json()

    sold = []

    for item in data.get("itemSummaries", []):
        try:
            sold.append({
                "price": float(item["price"]["value"]),
                "title": item["title"]
            })
        except:
            continue

    return sold

def calculate_market_price(sold):
    if not sold:
        return None

    prices = [s["price"] for s in sold]
    avg = sum(prices) / len(prices)

    return round(avg, 2)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DATABASE ----------------
def db():
    return psycopg2.connect(os.getenv("DB_URL"))

# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"status": "OmniSuite Running"}

# ---------------- CLOUDINARY UPLOAD ----------------
def upload_to_cloudinary(image_bytes):
    url = f"https://api.cloudinary.com/v1_1/{os.getenv('CLOUDINARY_CLOUD_NAME')}/image/upload"

    files = {"file": image_bytes}
    data = {"upload_preset": "ml_default"}

    r = requests.post(url, files=files, data=data)
    return r.json()["secure_url"]

# ---------------- OPENAI VISION ----------------
def ai_vision(image_bytes):
    url = "https://api.openai.com/v1/responses"

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }

    image_base64 = base64.b64encode(image_bytes).decode()

    data = {
        "model": "gpt-4.1-mini",
        "input": [{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Identify this product exactly (sports card: year, brand, player, number)."},
                {"type": "input_image", "image_base64": image_base64}
            ]
        }]
    }

    r = requests.post(url, headers=headers, json=data)
    return r.json()["output"][0]["content"][0]["text"]

# ---------------- ALIEXPRESS SEARCH ----------------
def aliexpress_search(image_url):
    url = "https://aliexpress-datahub.p.rapidapi.com/item_search_image"

    headers = {
        "x-rapidapi-key": os.getenv("RAPID_API_KEY_ALIEXPRESS"),
        "x-rapidapi-host": "aliexpress-datahub.p.rapidapi.com"
    }

    params = {
        "sort": "default",
        "catId": "0",
        "imgUrl": image_url
    }

    r = requests.get(url, headers=headers, params=params)
    data = r.json()

    results = []

    for item in data.get("data", [])[:5]:
        try:
            results.append({
                "title": item.get("title"),
                "price": float(item.get("price", 0)),
                "image": item.get("image"),
                "url": item.get("itemUrl")
            })
        except:
            continue

    return results

# ---------------- PROFIT ENGINE ----------------
def calculate_profit(suppliers):
    if not suppliers:
        return None

    best = min(suppliers, key=lambda x: x["price"])

    return {
        "best_cost": best["price"],
        "recommended_price": round(best["price"] * 2.2, 2),
        "profit": round(best["price"] * 1.2, 2),
        "supplier": best
    }

# ---------------- MAIN AI PIPELINE ----------------
@app.post("/ai/scan")
async def scan(file: UploadFile = File(...)):
    image_bytes = await file.read()

    # 1. Upload image
    image_url = upload_to_cloudinary(image_bytes)

    # 2. AI identify
    product_name = ai_vision(image_bytes)

    # 3. Supplier (cost)
    suppliers = aliexpress_search(image_url)

    # 4. eBay sold comps
    sold = ebay_sold_search(product_name)

    # 5. Market price
    market_price = calculate_market_price(sold)

    # 6. Best supplier
    best_cost = min([s["price"] for s in suppliers]) if suppliers else 0

    profit = market_price - best_cost if market_price else 0

    return {
        "product_name": product_name,
        "image_url": image_url,
        "suppliers": suppliers,
        "sold_comps": sold,
        "market_price": market_price,
        "best_cost": best_cost,
        "profit": profit
    }
@app.post("/listings/auto-create")
def auto_create(data: dict):
    conn = db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO listings(title, price, cost) VALUES (%s,%s,%s) RETURNING id;",
        (data["title"], data["price"], data["cost"])
    )

    new_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return {"id": new_id}
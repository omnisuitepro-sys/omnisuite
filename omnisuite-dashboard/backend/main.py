from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.finance.omni_alpha_routes import app as alpha_finance_app

# =========================================================
# ✅ FASTAPI APPLICATION INIT
# =========================================================
app = FastAPI(
    title="OmniSuite API",
    description="Core backend API for OmniMirror + OmniSuite dashboard.",
    version="1.0.0",
)

# =========================================================
# ✅ CORS CONFIGURATION (Updated)
# =========================================================
origins = [
    "http://localhost:3000",                  # Local development dashboard
    "https://dashboard.getomnirecall.com",    # Production dashboard
    "https://api.getomnirecall.com",          # Render/Backend API
]

# Optional: wildcard subdomain support for future staging (e.g. beta, dev)
# from starlette.middleware.cors import CORSMiddleware
# origins.append("https://*.getomnirecall.com")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],       # Allow everything for now
    allow_headers=["*"],       # In production you can restrict if needed
)

# =========================================================
# ✅ ROOT ROUTE
# =========================================================
@app.get("/", response_class=JSONResponse)
async def root():
    return {"status": "ok", "message": "OmniSuite API is operational 👋"}

@app.get("/listings")
def get_listings():
    return [
        {"id": 1, "title": "iPhone Case", "price": 12.99},
        {"id": 2, "title": "Wireless Mouse", "price": 24.99},
        {"id": 3, "title": "LED Desk Lamp", "price": 34.99},
    ]

# =========================================================
# ✅ STATUS / HEALTH CHECK ENDPOINT
# =========================================================
@app.get("/health", response_class=JSONResponse)
async def health_check():
    return {"status": "healthy", "api": "FastAPI running on Render", "message": "OK"}

# =========================================================
# ✅ INCLUDE SUBMODULES / ROUTERS
# =========================================================
app.mount("/alpha", alpha_finance_app)

# =========================================================
# ✅ APPLICATION RUN (for local testing only)
# =========================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=10000,    # Port dynamically assigned on Render at runtime
        reload=True
    )
# ==============================================================
#  OmniSuite Beta Tier and License Module
# ==============================================================
import json, os, datetime

LIC_FILE = "licenses.json"

DEFAULT_TIERS = {
    "Free": {
        "import_limit": 25,
        "auto_reprice": False,
        "multi_market": False,
        "hourly_sync": False,
        "ml_optimizer": False,
        "auto_order": False
    },
    "Basic": {
        "import_limit": 200,
        "auto_reprice": True,
        "multi_market": True,
        "hourly_sync": False,
        "ml_optimizer": False,
        "auto_order": False
    },
    "Pro": {
        "import_limit": 1000,
        "auto_reprice": True,
        "multi_market": True,
        "hourly_sync": True,
        "ml_optimizer": True,
        "auto_order": True
    },
    "Enterprise": {
        "import_limit": 999999,
        "auto_reprice": True,
        "multi_market": True,
        "hourly_sync": True,
        "ml_optimizer": True,
        "auto_order": True
    }
}

def load_licenses():
    if not os.path.exists(LIC_FILE):
        json.dump({}, open(LIC_FILE, "w"))
    with open(LIC_FILE, "r") as f:
        data = json.load(f)
    return data

def save_license(lic_data):
    with open(LIC_FILE, "w") as f:
        json.dump(lic_data, f, indent=2)

def get_tier(username: str):
    licenses = load_licenses()
    if username not in licenses:
        return "Free"
    record = licenses[username]
    expiry = datetime.datetime.fromisoformat(record["expiry"])
    if expiry < datetime.datetime.utcnow():
        return "Free"
    return record["tier"]

def new_license(username: str, tier: str, days: int = 30):
    licenses = load_licenses()
    expiry = (datetime.datetime.utcnow() + datetime.timedelta(days=days)).isoformat()
    licenses[username] = {"tier": tier, "expiry": expiry}
    save_license(licenses)
    return {"user": username, "tier": tier, "expiry": expiry}
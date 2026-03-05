# ------------------------------------------------------------
# plaid_utils.py  —  Omni Alpha Financial Plaid integration tools
# ------------------------------------------------------------
import os
from datetime import datetime, timedelta
from plaid import Configuration, ApiClient, Environment
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest

# --------------------------------------------------------------------
# Environment setup
# --------------------------------------------------------------------
PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")  # sandbox | development | production

# Determine which Plaid environment to use
def _get_plaid_client():
    host = {
        "sandbox": Environment.Sandbox,
        "development": Environment.Development,
        "production": Environment.Production,
    }.get(PLAID_ENV.lower(), Environment.Sandbox)

    configuration = Configuration(
        host=host,
        api_key={"clientId": PLAID_CLIENT_ID, "secret": PLAID_SECRET},
    )
    api_client = ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)

# ------------------------------------------------------------
# Transaction & Subscription Logic
# ------------------------------------------------------------
def get_monthly_subscriptions(access_token: str):
    """
    Pull past‑30‑day transactions from Plaid and return
    any recurring merchant names as subscription candidates.
    """
    client = _get_plaid_client()
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)

    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=start_date.date(),
        end_date=end_date.date()
    )
    response = client.transactions_get(request)
    txns = response["transactions"]

    # Simple pattern detection for repeating merchants
    merchants = {}
    for txn in txns:
        name = txn["name"]
        merchants.setdefault(name, 0)
        merchants[name] += 1

    subscriptions = []
    for name, count in merchants.items():
        if count >= 2:  # Appears more than once per month
            amount = next(
                (t["amount"] for t in txns if t["name"] == name), None
            )
            subscriptions.append({
                "name": name,
                "frequency": "monthly",
                "average_amount": amount,
            })

    return subscriptions


# ------------------------------------------------------------
# Balances
# ------------------------------------------------------------
def get_total_balance(access_token: str) -> float:
    """
    Retrieve total available balance across all accounts.
    """
    client = _get_plaid_client()
    request = AccountsBalanceGetRequest(access_token=access_token)
    response = client.accounts_balance_get(request)
    balances = [
        acct["balances"]["available"] or acct["balances"]["current"]
        for acct in response["accounts"]
    ]
    return round(sum(balances), 2)


# ------------------------------------------------------------
# Persistence helper
# ------------------------------------------------------------
def save_subscriptions_to_db(subscriptions, user_id, db):
    """
    Save detected subscriptions to your local database.
    Replace this stub with your ORM model logic as needed.
    """
    try:
        for sub in subscriptions:
            db.execute(
                """
                INSERT INTO subscriptions (user_id, merchant_name, frequency, avg_amount)
                VALUES (:uid, :merchant, :freq, :amount)
                """,
                {
                    "uid": user_id,
                    "merchant": sub.get("name"),
                    "freq": sub.get("frequency"),
                    "amount": sub.get("average_amount"),
                },
            )
        db.commit()
        return f"{len(subscriptions)} subscriptions saved for {user_id}"
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"DB write failed: {e}")
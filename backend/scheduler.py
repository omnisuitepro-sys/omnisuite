import time
import threading
import logging
from datetime import datetime
from backend.tiers import load_licenses, get_tier, DEFAULT_TIERS

logging.basicConfig(
    filename="scheduler.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def hourly_sync_task(username: str):
    """Simulate Enterprise-only hourly sync and ML optimizer."""
    logging.info(f"⚙️ Hourly Sync Start — user: {username}")
    time.sleep(3)  # simulate processing
    logging.info(f"✅ Sync complete for {username} at {datetime.utcnow().isoformat()}")

def enterprise_scheduler():
    """Runs hourly tasks for Enterprise-tier users."""
    while True:
        try:
            licenses = load_licenses()
            for user, data in licenses.items():
                if data["tier"] == "Enterprise":
                    threading.Thread(
                        target=hourly_sync_task,
                        args=(user,),
                        daemon=True
                    ).start()
        except Exception as e:
            logging.error(f"Scheduler error: {e}")
        time.sleep(3600)  # run every hour
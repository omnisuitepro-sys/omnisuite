import os, time, subprocess, logging

logging.basicConfig(filename="auto_repair.log",
                    level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")

def monitor_services():
    """Checks if main server (Uvicorn) is running; restarts if crashed."""
    while True:
        try:
            # `tasklist` works on Windows to check if a process exists
            tasks = subprocess.check_output("tasklist", text=True)
            if "uvicorn.exe" not in tasks and "python.exe" not in tasks:
                logging.warning("Main service stopped — restarting.")
                os.system("start cmd /c uvicorn backend.main:app --reload")
        except Exception as e:
            logging.error(f"Auto‑repair error: {e}")
        time.sleep(60)
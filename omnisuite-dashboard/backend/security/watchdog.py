import psutil, time, statistics, logging

logging.basicConfig(filename="watchdog.log",
                    level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")

def system_watchdog():
    """Monitors CPU usage for anomalies."""
    window = []
    while True:
        try:
            cpu = psutil.cpu_percent(interval=1)
            window.append(cpu)
            if len(window) > 30:
                avg = statistics.mean(window[-30:])
                stdev = statistics.stdev(window[-30:]) or 1
                if abs(cpu - avg) > 3 * stdev:
                    logging.warning(f"⚠️ CPU anomaly detected: {cpu}%  avg:{avg:.1f}%")
            time.sleep(10)
        except Exception as e:
            logging.error(f"Watchdog error: {e}")

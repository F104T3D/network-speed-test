import socket
import time
import requests
import logging
import concurrent.futures

LOG_FILE = "speedtest.log"

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def log(msg):
    logging.info(msg)

def ping_test(host="1.1.1.1", port=443, timeout=2):
    try:
        start = time.time()
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        end = time.time()
        s.close()
        latency = (end - start) * 1000
        log(f"Ping: {latency:.2f} ms")
        return latency
    except Exception as e:
        log(f"Ping failed: {e}")
        return None

def download_worker(url):
    try:
        r = requests.get(url, stream=True, timeout=10)
        total_bytes = 0
        for chunk in r.iter_content(1024 * 1024):  # 1MB
            total_bytes += len(chunk)
        return total_bytes
    except Exception as e:
        log(f"Download thread error: {e}")
        return 0

def download_test(url="http://ipv4.download.thinkbroadband.com/100MB.zip", threads=4):
    log(f"Running download test with {threads} threads...")
    start = time.time()
    total_bytes = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(download_worker, url) for _ in range(threads)]
        for future in concurrent.futures.as_completed(futures):
            total_bytes += future.result()
    end = time.time()
    duration = end - start
    speed_mbps = (total_bytes * 8) / (duration * 1024 * 1024)
    log(f"Download speed: {speed_mbps:.2f} Mbps")
    return speed_mbps

def upload_test(url="https://httpbin.org/post", data_size_mb=10, threads=4):
    log(f"Running upload test with {threads} threads...")
    data = b'x' * (data_size_mb * 1024 * 1024)
    start = time.time()

    def upload_worker():
        try:
            r = requests.post(url, data=data, timeout=10)
            return len(data)
        except Exception as e:
            log(f"Upload thread error: {e}")
            return 0

    total_bytes = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(upload_worker) for _ in range(threads)]
        for future in concurrent.futures.as_completed(futures):
            total_bytes += future.result()
    end = time.time()
    duration = end - start
    speed_mbps = (total_bytes * 8) / (duration * 1024 * 1024)
    log(f"Upload speed: {speed_mbps:.2f} Mbps")
    return speed_mbps

def main():
    log("=== Starting Speed Test ===")
    ping_test()
    download_test()
    upload_test()
    log("=== Speed Test Completed ===")

if __name__ == "__main__":
    main()

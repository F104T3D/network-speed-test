import socket
import time
import requests
import logging

LOG_FILE = "speedtest.log"

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def ping_test(host="1.1.1.1", port=443, timeout=2):
    try:
        start = time.time()
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        end = time.time()
        s.close()
        latency = (end - start) * 1000
        print(f"Ping: {latency:.2f} ms")
        return latency
    except Exception as e:
        print(f"Ping failed: {e}")
        return None

def download_test(url="http://ipv4.download.thinkbroadband.com/10MB.zip"):
    try:
        start = time.time()
        r = requests.get(url, stream=True)
        total_bytes = 0
        for chunk in r.iter_content(1024 * 1024):
            total_bytes += len(chunk)
        end = time.time()
        duration = end - start
        speed_mbps = (total_bytes * 8) / (duration * 1024 * 1024)
        print(f"Download speed: {speed_mbps:.2f} Mbps")
        return speed_mbps
    except Exception as e:
        print(f"Download failed: {e}")
        return None

def upload_test(url="https://httpbin.org/post", data_size_mb=5):
    try:
        data = b'x' * (data_size_mb * 1024 * 1024)
        start = time.time()
        r = requests.post(url, data=data)
        end = time.time()
        duration = end - start
        speed_mbps = (len(data) * 8) / (duration * 1024 * 1024)
        print(f"Upload speed: {speed_mbps:.2f} Mbps")
        return speed_mbps
    except Exception as e:
        print(f"Upload failed: {e}")
        return None

def main():
    ping_test()
    download_test()
    upload_test()
    print("Completed")

if __name__ == "__main__":
    main()

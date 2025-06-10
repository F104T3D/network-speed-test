# Python Network Speed Test

A simple Python script to test your internet connection speed.  
It measures:

-  Ping (latency to Cloudflare)
-  Download speed (multi-threaded)
-  Upload speed (multi-threaded)
-  Logs results to console and `speedtest.log`

## Requirements

- Python 3.6+
- `requests` library

Install with:

```bash
pip install requests
```
Usage

Run the script from your terminal:
```bash
python speedtest.py
```
Notes

    Uses Cloudflare (1.1.1.1) for ping.
    Downloads a test file from ThinkBroadband.
    Uploads test data to httpbin.org.

- Upload test may be limited by the test server's capacity.

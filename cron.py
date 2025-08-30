import os, requests, time

API_URL = os.getenv("CRON_API_URL", "https://app.tangtheodoi.net/cron/cronauto.php").strip()
UPDATE_URL = os.getenv("CRON_UPDATE_URL", "https://app.tangtheodoi.net/cron/time.php").strip()
session = requests.Session()

def fetch_jobs():
    try:
        r = session.get(API_URL, timeout=10)
        r.raise_for_status()
        data = r.json()
        return data if isinstance(data, list) else []
    except Exception as e:
        print("Fetch jobs error:", e)
        return []

def update_job(url, status_code):
    try:
        session.get(f"{UPDATE_URL}?url={requests.utils.quote(url, safe='')}&code={status_code}", timeout=8)
    except Exception as e:
        print("Update error:", e)

while True:
    jobs = fetch_jobs()
    now = int(time.time())
    count = 0
    for item in jobs:
        try:
            sogiay = int(item.get('sogiay', 60))
            time_his = int(item.get('time_his', 0))
            if (now - time_his) < sogiay:
                continue
            url = item.get('url', '').strip()
            if not url:
                continue
            method = str(item.get('phuongthuc', 'GET')).upper()
            resp = session.post(url, timeout=8) if method == 'POST' else session.get(url, timeout=8)
            print(f"URL: {url} -> {resp.status_code}")
            update_job(url, resp.status_code)
            count += 1
        except Exception as e:
            print("Run item error:", e)
    print(f"Ran {count} job(s)")
    time.sleep(2)

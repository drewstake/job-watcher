from dotenv import load_dotenv
# Override shell exports with .env values
load_dotenv(override=True)

import os
import sys
import json
import time
import smtplib
from datetime import datetime
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# — CONFIG —
BASE_URL      = "https://recruiting.paylocity.com"
PATH          = "/recruiting/jobs/All/4e1cd2fd-3e15-41ae-a6d5-1ca70a95426b/Elite-Development-Group-LLC"
URL           = BASE_URL + PATH
SEEN_FILE     = "seen.json"
TO_EMAIL      = "drewstake3@gmail.com"
DATE_FORMAT   = "%Y-%m-%d"

REQUIRED_ENVS = [
    "SMTP_HOST",
    "SMTP_PORT",
    "SMTP_USER",
    "SMTP_PASS",
    "SENDER_EMAIL",
    "REPLY_TO_EMAIL"
]

def check_env_vars():
    missing = [v for v in REQUIRED_ENVS if not os.getenv(v)]
    if missing:
        print("Error: missing environment variables:", ", ".join(missing))
        sys.exit(1)

def load_seen():
    """
    Load a dict of {url: first_seen_date} from seen.json.
    Supports legacy list format by migrating into a dict with today’s date.
    """
    try:
        raw = json.load(open(SEEN_FILE))
    except FileNotFoundError:
        return {}

    if isinstance(raw, list):
        today = datetime.now().strftime(DATE_FORMAT)
        return {url: today for url in raw}
    elif isinstance(raw, dict):
        return raw
    else:
        return {}

def save_seen(seen_dict):
    with open(SEEN_FILE, "w") as f:
        json.dump(seen_dict, f, indent=2)

def fetch_jobs():
    opts = Options()
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=opts
    )
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"}
    )

    driver.get(URL)
    time.sleep(5)

    jobs = []
    for card in driver.find_elements(By.CSS_SELECTOR, ".job-listing-job-item"):
        link_el = card.find_element(By.CSS_SELECTOR, ".job-item-title a")
        title   = link_el.text.strip()
        href    = link_el.get_attribute("href")
        url     = href if href.startswith("http") else BASE_URL + href
        jobs.append({"title": title, "url": url})
    driver.quit()
    return jobs

def send_email(new_jobs):
    body = "\n\n".join(f"{j['title']}\n{j['url']}" for j in new_jobs)
    msg = EmailMessage()
    msg["Subject"]  = f"{len(new_jobs)} new job(s) found"
    msg["From"]     = os.getenv("SENDER_EMAIL")
    msg["Reply-To"] = os.getenv("REPLY_TO_EMAIL")
    msg["To"]       = TO_EMAIL
    msg.set_content(body)

    with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as smtp:
        smtp.starttls()
        smtp.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
        smtp.send_message(msg)

def main():
    check_env_vars()

    seen     = load_seen()
    jobs     = fetch_jobs()
    today    = datetime.now().strftime(DATE_FORMAT)

    print(f"\n=== Current Jobs ({len(jobs)}) ===")
    for i, job in enumerate(jobs, 1):
        mark = seen.get(job["url"], "NEW")
        print(f"{i}. {job['title']}  (first seen: {mark})\n   {job['url']}")
    print("=" * 30 + "\n")

    new_jobs = [j for j in jobs if j["url"] not in seen]
    if not new_jobs:
        print("No new jobs found.\n")
        return

    send_email(new_jobs)
    for j in new_jobs:
        seen[j["url"]] = today
    save_seen(seen)
    print(f"Sent email for {len(new_jobs)} new job(s) on {today}.\n")

if __name__ == "__main__":
    main()

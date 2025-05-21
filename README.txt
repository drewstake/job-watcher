```
README.txt

Project: Job Watcher
────────────────────

1. Purpose
   • Automate the monitoring of Elite Development Group’s Paylocity careers page  
   • Fetch new job listings every 12 hours and notify via email  
   • Saves time vs. manual checking and demonstrates proactive tooling

2. Motivation / Interview Talking Point
   After two interviews with a company, I was told to “keep an eye on our Careers page.”  
   Rather than manually reloading the site, I wrote this script to:
     – Scrape the live listings  
     – Diff against previously seen jobs  
     – Email me any new openings  
   It’s a real-world example of solving a tedious workflow with automation,  
   and showcases skills in web scraping, serverless scheduling, and SMTP integration.

3. Tech Stack
   • Language: Python 3.13  
   • Web Scraping: Selenium + Headless Chrome (chromedriver via webdriver-manager)  
   • Email Relay: SendGrid SMTP API (“apikey” as SMTP user)  
   • Environment:  
       – Virtualenv (`venv`) for dependency isolation  
       – `python-dotenv` for loading `.env` secrets  
   • Scheduler:  
       – GitHub Actions workflow, runs at 8 AM & 8 PM EDT (cron: `0 */12 * * *`).  
   • Persistence:  
       – Local JSON file (`seen.json`) to track which URLs have been emailed  

4. File Structure
   ├── job_watcher.py      # Main script: fetch, diff, email  
   ├── .env                # (git-ignored) SMTP & sender config  
   ├── seen.json           # Runtime: stores seen job URLs  
   ├── .github/            # GitHub Actions config  
   │   └── workflows/  
   │       └── job-watcher.yml  
   ├── requirements.txt    # pip dependencies  
   ├── .gitignore          # excludes venv, .env, seen.json, cache  
   └── README.txt          # This file

5. Environment Variables (`.env`)
```

SMTP\_HOST=smtp.sendgrid.net
SMTP\_PORT=587
SMTP\_USER=apikey
SMTP\_PASS=\<YOUR\_SENDGRID\_API\_KEY>
SENDER\_EMAIL=[proxypham@gmail.com](mailto:proxypham@gmail.com)
REPLY\_TO\_EMAIL=[drewstake3@gmail.com](mailto:drewstake3@gmail.com)

```

6. Installation & Usage
1. Clone repo and `cd job-watcher`  
2. `python3 -m venv venv && source venv/bin/activate`  
3. `pip install -r requirements.txt`  
4. Create & populate `.env` as above  
5. Test: `python job_watcher.py` (should print 4 current jobs and send email)  
6. Commit & push; GitHub Actions will auto-run twice daily

7. Interview Highlights
• Demonstrates end-to-end automation: scraping → diff → notification  
• Shows handling of real-world website in JS-heavy environment via Selenium  
• Leverages serverless CI/CD (GitHub Actions) as a scheduler  
• Secure credential management with `.env` + python-dotenv  
• Persists minimal state locally (JSON), keeping design simple  

────────────────────  
Author: Andrew Nguyen  
```

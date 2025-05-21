# Job Watcher

Periodic scraper that checks for new job listings on a Paylocity page and emails you when new ones appear.

## Setup

1. Clone this repo and `cd job-watcher`
2. Create an SMTP app password (e.g. Gmail) and export as env-vars:
   ```bash
   export SMTP_HOST=smtp.gmail.com
   export SMTP_PORT=587
   export SMTP_USER=you@yourdomain.com
   export SMTP_PASS=your_app_password

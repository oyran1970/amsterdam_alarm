import os
from datetime import datetime
from pathlib import Path
import requests
from playwright.sync_api import sync_playwright
from twilio.rest import Client

# ------------------------
# Konfigurasjon
# ------------------------
TICKET_URL = "https://atleta.cc/e/nhIVWn50Rcez/resale"
LOG_URL = "https://oyran1970.github.io/amsterdam_alarm/log/ticket_checker.log"

# Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM")
TWILIO_TO = os.getenv("TWILIO_TO")

# Lokalt logg
LOG_DIR = Path("log")
LOG_DIR.mkdir(exist_ok=True)
LOCAL_LOG_FILE = LOG_DIR / "ticket_checker.log"

# ------------------------
# Hent billettstatus
# ------------------------
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(TICKET_URL)
    try:
        page.wait_for_selector(".available", timeout=5000)
        page.wait_for_selector(".sold", timeout=5000)
    except:
        print("Fant ikke .available eller .sold på siden")
        browser.close()
        exit(1)

    available = int(page.query_selector(".available").inner_text().strip())
    sold = int(page.query_selector(".sold").inner_text().strip())
    browser.close()

# ------------------------
# Timestamp
# ------------------------
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# ------------------------
# Logg til lokalt fil
# ------------------------
with open(LOCAL_LOG_FILE, "a") as f:
    f.write(f"{timestamp}, Available: {available}, Sold: {sold}\n")

print(f"Logged locally: {available} available, {sold} sold")

# ------------------------
# Logg til GitHub Pages URL
# ------------------------
try:
    log_entry = f"{timestamp}, Available: {available}, Sold: {sold}\n"
    response = requests.post(LOG_URL, data=log_entry)
    if response.ok:
        print(f"Logged to URL: {LOG_URL}")
    else:
        print(f"Kunne ikke logge til URL, status: {response.status_code}")
except Exception as e:
    print(f"Kunne ikke sende log: {e}")

# ------------------------
# SMS-varsling ved ledige billetter
# ------------------------
if available > 0 and all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM, TWILIO_TO]):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = f"Det finnes nå {available} billetter! Solgt: {sold}. Sjekk {TICKET_URL}"
    try:
        sms = client.messages.create(
            body=message,
            from_=TWILIO_FROM,
            to=TWILIO_TO
        )
        print(f"SMS sendt, SID: {sms.sid}")
    except Exception as e:
        print(f"Feilet å sende SMS: {e}")

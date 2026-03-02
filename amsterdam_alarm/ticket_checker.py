# amsterdam_alarm/ticket_checker.py

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import datetime
from twilio.rest import Client

# Twilio-konfigurasjon (behold dine eksisterende verdier)
account_sid = "YOUR_TWILIO_SID"
auth_token = "YOUR_TWILIO_TOKEN"
from_number = "+1234567890"
to_number = "+0987654321"

# URL for billettsiden
ticket_url = "URL_TIL_BILLETSIDE"
# URL for loggfil (GitHub Pages)
log_url = "https://oyran1970.github.io/amsterdam_alarm/log/ticket_checker.log"

# Hent HTML med Playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(ticket_url)
    html = page.content()
    browser.close()

soup = BeautifulSoup(html, "html.parser")

# Sjekk om .available og .sold finnes
available_elem = soup.select_one(".available")
sold_elem = soup.select_one(".sold")

if available_elem and sold_elem:
    available = int(available_elem.text.strip())
    sold = int(sold_elem.text.strip())
    print(f"Available: {available}, Sold: {sold}")
else:
    print("Fant ikke .available eller .sold på siden")
    available = sold = None

# Logg til GitHub Pages (legg til ny rad med timestamp)
timestamp = datetime.datetime.now().isoformat()
log_line = f"{timestamp}, Available: {available}, Sold: {sold}\n"

try:
    r = requests.get(log_url)
    if r.status_code == 200:
        log_content = r.text + log_line
        # Skriv tilbake til GitHub (du kan bruke push action som før)
        with open("log/ticket_checker.log", "a") as f:
            f.write(log_line)
except Exception as e:
    print("Kunne ikke sende log:", e)

# Send SMS hvis billetter tilgjengelig
if available and available > 0:
    client = Client(account_sid, auth_token)
    message = f"Billett(er) tilgjengelig: {available}"
    client.messages.create(body=message, from_=from_number, to=to_number)
    print("SMS sendt")

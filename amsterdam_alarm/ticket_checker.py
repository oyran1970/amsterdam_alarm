import requests
from bs4 import BeautifulSoup
from datetime import datetime
from twilio.rest import Client
import os

# ---------- KONFIGURASJON ----------
URL = "https://atleta.cc/e/nhIVWn50Rcez/resale"
LOG_FILE = "log/ticket_checker.log"  # må eksistere som mappe
TWILIO_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER")
TO_NUMBER = os.environ.get("TWILIO_TO_NUMBER")
# -----------------------------------

def check_tickets():
    resp = requests.get(URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Finn elementene med ticket info (tilpass etter riktig HTML)
    available = sold = 0
    for item in soup.select(".ticket-info"):  # tilpass selector
        text = item.get_text()
        if "Available" in text:
            available = int(text.split()[0])
        elif "Sold" in text:
            sold = int(text.split()[0])
    return available, sold

def log_tickets(available, sold):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"{timestamp} | Available: {available} | Sold: {sold}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)
    print(f"Logged: {line.strip()}")

def send_sms(available):
    if available > 0 and all([TWILIO_SID, TWILIO_TOKEN, FROM_NUMBER, TO_NUMBER]):
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        msg = f"Tickets available! ({available} left)"
        client.messages.create(body=msg, from_=FROM_NUMBER, to=TO_NUMBER)
        print("SMS sent!")

if __name__ == "__main__":
    try:
        available, sold = check_tickets()
        log_tickets(available, sold)
        send_sms(available)
    except Exception as e:
        print("Error:", e)

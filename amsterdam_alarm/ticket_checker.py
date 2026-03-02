import requests
from bs4 import BeautifulSoup
from datetime import datetime
from twilio.rest import Client

# Konfigurasjon
TICKET_URL = "https://atleta.cc/e/nhIVWn50Rcez/resale"
LOG_URL = "https://your-log-endpoint.com/log"  # Sett inn din faste logg-URL
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_FROM_NUMBER = "+1234567890"
TWILIO_TO_NUMBER = "+47xxxxxxxx"

def fetch_ticket_info():
    response = requests.get(TICKET_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Eksempel selectors – tilpass hvis nettsiden endrer seg
    available_text = soup.select_one(".available").get_text(strip=True)
    sold_text = soup.select_one(".sold").get_text(strip=True)

    available = int(available_text.split()[0])
    sold = int(sold_text.split()[0])
    return available, sold

def log_to_url(timestamp, available, sold):
    payload = {
        "timestamp": timestamp,
        "available": available,
        "sold": sold
    }
    try:
        response = requests.post(LOG_URL, json=payload)
        response.raise_for_status()
        print(f"Logged to URL: {payload}")
    except Exception as e:
        print(f"Kunne ikke sende log: {e}")

def send_sms(available):
    if available > 0:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Billett tilgjengelig! {available} ledige.",
            from_=TWILIO_FROM_NUMBER,
            to=TWILIO_TO_NUMBER
        )
        print(f"SMS sendt: {message.sid}")

def main():
    try:
        available, sold = fetch_ticket_info()
        timestamp = datetime.utcnow().isoformat()
        log_to_url(timestamp, available, sold)
        send_sms(available)
    except Exception as e:
        print(f"Feil under kjøring: {e}")

if __name__ == "__main__":
    main()

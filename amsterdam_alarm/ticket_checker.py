import requests
from bs4 import BeautifulSoup
from datetime import datetime
from twilio.rest import Client

# --- KONFIGURASJON ---
URL = "https://atleta.cc/e/nhIVWn50Rcez/resale"
LOG_ENDPOINT = "https://your-log-endpoint.com/log"  # Sett inn din faste logg-URL
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_FROM_NUMBER = "+1234567890"
TWILIO_TO_NUMBER = "+47XXXXXXXX"

# --- FUNKSJONER ---
def send_sms(message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=TWILIO_TO_NUMBER
        )
        print("SMS sendt:", message)
    except Exception as e:
        print("Kunne ikke sende SMS:", e)

def log_to_url(timestamp, available, sold):
    try:
        data = {"timestamp": timestamp, "available": available, "sold": sold}
        resp = requests.post(LOG_ENDPOINT, json=data, timeout=10)
        resp.raise_for_status()
        print(f"Logget til URL: {data}")
    except Exception as e:
        print(f"Kunne ikke sende log: {e}")
        # fallback til lokal fil
        try:
            import os
            os.makedirs("log", exist_ok=True)
            with open("log/ticket_checker.log", "a") as f:
                f.write(f"{timestamp} | Available: {available} | Sold: {sold}\n")
            print(f"Logget til lokal fil: {timestamp} | {available} | {sold}")
        except Exception as e2:
            print("Kunne ikke logge til lokal fil:", e2)

def parse_ticket_info(html):
    soup = BeautifulSoup(html, "html.parser")
    # Tilpass selector etter faktiske nettside-elementer
    available_elem = soup.find("span", {"id": "available"})
    sold_elem = soup.find("span", {"id": "sold"})
    available = int(available_elem.text.strip()) if available_elem else 0
    sold = int(sold_elem.text.strip()) if sold_elem else 0
    return available, sold

# --- HOVEDLOGIKK ---
def main():
    try:
        r = requests.get(URL, timeout=10)
        r.raise_for_status()
        available, sold = parse_ticket_info(r.text)
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        log_to_url(timestamp, available, sold)

        if available > 0:
            send_sms(f"Billett tilgjengelig! {available} ledige, {sold} solgt. {URL}")

        print(f"Ferdig kjøring: {timestamp} | Available: {available} | Sold: {sold}")

    except Exception as e:
        print("Feil under kjøring:", e)

if __name__ == "__main__":
    main()

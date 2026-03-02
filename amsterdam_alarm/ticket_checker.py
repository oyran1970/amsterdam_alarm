import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from twilio.rest import Client

# -------------------------------
# Konfigurasjon
# -------------------------------
URL = "https://atleta.cc/e/nhIVWn50Rcez/resale"
LOG_DIR = "log"
LOG_FILE = os.path.join(LOG_DIR, "ticket_checker.log")

# Twilio (valgfritt)
TWILIO_ENABLED = True
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_FROM = "+1234567890"
TWILIO_TO = "+9876543210"

# -------------------------------
# Opprett log-mappen om nødvendig
# -------------------------------
os.makedirs(LOG_DIR, exist_ok=True)

# -------------------------------
# Funksjon for logging
# -------------------------------
def log_status(available, sold):
    timestamp = datetime.utcnow().strftime("%a %b %d %H:%M:%S UTC %Y")
    log_line = f"{timestamp} | Available: {available} | Sold: {sold}\n"
    
    # Skriv til loggfil
    with open(LOG_FILE, "a") as f:
        f.write(log_line)
    
    # Print til konsoll
    print(log_line)

# -------------------------------
# Funksjon for å hente billettstatus
# -------------------------------
def check_tickets():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(URL)
        
        # Eksempel på hvordan vi henter antall billetter
        # Tilpass selektorer etter nettsidens HTML
        available_text = page.query_selector("selector_for_available").inner_text()
        sold_text = page.query_selector("selector_for_sold").inner_text()
        
        # Konverter til tall
        available = int(available_text.strip())
        sold = int(sold_text.strip())
        
        browser.close()
        return available, sold

# -------------------------------
# Funksjon for å sende SMS
# -------------------------------
def send_sms(message):
    if not TWILIO_ENABLED:
        return
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_FROM,
        to=TWILIO_TO
    )

# -------------------------------
# Hovedprogram
# -------------------------------
def main():
    try:
        available, sold = check_tickets()
        log_status(available, sold)
        
        # Varsle hvis billetter tilgjengelig
        if available > 0:
            send_sms(f"Billetter tilgjengelig! Available: {available}, Sold: {sold}")
            
    except Exception as e:
        print(f"Feil under sjekk: {e}")
        log_status(available=0, sold=0)

if __name__ == "__main__":
    main()

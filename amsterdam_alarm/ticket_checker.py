from playwright.sync_api import sync_playwright
from twilio.rest import Client
import os
print("Ticket checker starter...")

try:
    # Hele eksisterende kode for Playwright + Twilio
    ...
except Exception as e:
    print(f"Exception fanget: {e}")
    
# --- Konfigurasjon ---
TICKET_URL = "https://www.tcsamsterdammarathon.eu/ticket-resale"

# Hent Twilio-miljøvariabler
sid = os.getenv("TWILIO_SID")
token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_NUMBER")
to_number = os.getenv("YOUR_NUMBER")

# --- Sjekk tickets ---
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(TICKET_URL)
        
        # Sjekk om "tickets available" finnes på siden
        if "Tickets available" in page.content():
            print("Billetter er tilgjengelige!")

            # --- Send SMS via Twilio ---
            if all([sid, token, from_number, to_number]):
                client = Client(sid, token)
                message = client.messages.create(
                    body="Amsterdam Maraton: Billetter tilgjengelige! Gå til " + TICKET_URL,
                    from_=from_number,
                    to=to_number
                )
                print(f"SMS sendt, SID: {message.sid}")
            else:
                print("Twilio-miljøvariabler mangler, SMS ikke sendt")
        else:
            print("Ingen billetter tilgjengelige")
        
        browser.close()
except Exception as e:
    print(f"Feil under ticket-sjekk: {e}")

print("Ticket checker ferdig")

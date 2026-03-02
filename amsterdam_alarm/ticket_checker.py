from datetime import datetime
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

# Dine variabler
twilio_sid = "TWILIO_ACCOUNT_SID"
twilio_token = "TWILIO_AUTH_TOKEN"
twilio_from = "+1234567890"
twilio_to = "+47XXXXXXXX"
log_file = "log/ticket_checker.log"

# Hent siden
url = "https://atleta.cc/e/nhIVWn50Rcez/resale"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, "html.parser")

# Finn tilgjengelige og solgte billetter
available = int(soup.select_one(".available").text.strip())
sold = int(soup.select_one(".sold").text.strip())

# Legg til logglinje
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
with open(log_file, "a") as f:
    f.write(f"{timestamp}, Available: {available}, Sold: {sold}\n")

# Push til GitHub Pages skjer via workflow

# Send SMS hvis billetter tilgjengelig
if available > 0:
    client = Client(twilio_sid, twilio_token)
    client.messages.create(
        body=f"Tickets available: {available}",
        from_=twilio_from,
        to=twilio_to
    )

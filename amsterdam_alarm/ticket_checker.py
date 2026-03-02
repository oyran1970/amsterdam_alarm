import requests
from bs4 import BeautifulSoup
import datetime
import json

# --- Konfigurasjon ---
URL = "https://atleta.cc/e/nhIVWn50Rcez/resale"
LOG_ENDPOINT = "https://your-log-endpoint.com/log"  # <-- bytt til din URL

# --- Hent siden ---
response = requests.get(URL)
if response.status_code != 200:
    print(f"Feil ved henting av siden: {response.status_code}")
    exit(1)

soup = BeautifulSoup(response.text, "html.parser")

# --- Finn available og sold tickets ---
# Du må tilpasse selectorene til HTML-strukturen på siden
available_tag = soup.select_one(".available-count")  # eksempel: <span class="available-count">278</span>
sold_tag = soup.select_one(".sold-count")            # eksempel: <span class="sold-count">0</span>

available = int(available_tag.text.strip()) if available_tag else 0
sold = int(sold_tag.text.strip()) if sold_tag else 0

# --- Lag timestamp ---
timestamp = datetime.datetime.utcnow().isoformat()

# --- Oppdater logg via URL ---
log_data = {
    "timestamp": timestamp,
    "available": available,
    "sold": sold
}

try:
    r = requests.post(LOG_ENDPOINT, json=log_data)
    if r.status_code == 200:
        print(f"Logged: {available} available, {sold} sold at {timestamp}")
    else:
        print(f"Feil ved logging: {r.status_code} {r.text}")
except Exception as e:
    print(f"Kunne ikke sende log: {e}")

# --- Alternativ lokal logging (valgfritt) ---
with open("log/ticket_checker.log", "a") as f:
    f.write(f"{timestamp}, {available}, {sold}\n")

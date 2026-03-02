import requests
from bs4 import BeautifulSoup
import datetime
import os

# --- KONFIGURASJON ---
URL = "https://atleta.cc/e/nhIVWn50Rcez/resale"  # siden vi scrapes
LOG_ENDPOINT = None  # Sett til din URL hvis du har en, f.eks. "https://webhook.site/xxxx"

# --- SIKKER LOKAL LOGG ---
os.makedirs("log", exist_ok=True)  # lager logg-mappen hvis den ikke finnes

try:
    # --- HENT SIDEN ---
    response = requests.get(URL)
    response.raise_for_status()
except Exception as e:
    print(f"Feil ved henting av siden: {e}")
    exit(1)

soup = BeautifulSoup(response.text, "html.parser")

# --- FINN ANTALL LEDIGE OG SOLGTE BILLETTER ---
available_tag = soup.select_one(".available-count")  # oppdater med riktig CSS-selector
sold_tag = soup.select_one(".sold-count")            # oppdater med riktig CSS-selector

available = int(available_tag.text.strip()) if available_tag else 0
sold = int(sold_tag.text.strip()) if sold_tag else 0

# --- LAG TIMESTAMP ---
timestamp = datetime.datetime.utcnow().isoformat()

# --- LOGG TIL URL (VALGFRI) ---
if LOG_ENDPOINT:
    log_data = {"timestamp": timestamp, "available": available, "sold": sold}
    try:
        r = requests.post(LOG_ENDPOINT, json=log_data)
        if r.status_code == 200:
            print(f"Logged to URL: {available} available, {sold} sold at {timestamp}")
        else:
            print(f"Feil ved logging til URL: {r.status_code} {r.text}")
    except Exception as e:
        print(f"Kunne ikke sende log til URL: {e}")

# --- LOKAL LOGGING ---
log_file_path = "log/ticket_checker.log"
with open(log_file_path, "a") as f:
    f.write(f"{timestamp}, {available}, {sold}\n")
    print(f"Logged locally: {available} available, {sold} sold at {timestamp}")

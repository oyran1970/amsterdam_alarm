import requests
from datetime import datetime
from bs4 import BeautifulSoup
import os

# --- Konfigurasjon ---
LOG_FILE = "log/ticket_checker.log"
URL = "https://atleta.cc/e/nhIVWn50Rcez/resale"  # Sett inn riktig billett-URL

# --- Hent nettsiden ---
response = requests.get(URL)
if response.status_code != 200:
    print(f"Feil ved henting: {response.status_code}")
    exit(1)

soup = BeautifulSoup(response.text, "html.parser")

# --- Finn antall Available og Sold ---
# Tilpass selectorene under til hvordan nettsiden viser tallene
available_elem = soup.find("div", class_="available")
sold_elem = soup.find("div", class_="sold")

available = available_elem.text.strip() if available_elem else "0"
sold = sold_elem.text.strip() if sold_elem else "0"

# --- Lag timestamp ---
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# --- Sørg for at log-mappen finnes ---
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# --- Skriv til logg ---
with open(LOG_FILE, "a", encoding="utf-8") as f:
    f.write(f"{timestamp} | Available: {available} | Sold: {sold}\n")

print(f"Logget: {timestamp} | Available: {available} | Sold: {sold}")

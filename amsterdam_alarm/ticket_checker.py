import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# --- Konfigurasjon ---
URL = "https://atleta.cc/e/nhIVWn50Rcez/resale"
LOG_DIR = "log"
LOG_FILE = os.path.join(LOG_DIR, "ticket_checker.log")

# --- Hent siden ---
response = requests.get(URL)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

# --- Finn billetter ---
# Her må du justere selectors til det riktige HTML-elementet
available_tag = soup.select_one("#available")  # eksempel
sold_tag = soup.select_one("#sold")           # eksempel

available = int(available_tag.text.strip()) if available_tag else 0
sold = int(sold_tag.text.strip()) if sold_tag else 0

# --- Lag logg-mappen hvis den ikke finnes ---
os.makedirs(LOG_DIR, exist_ok=True)

# --- Skriv til logg ---
with open(LOG_FILE, "a") as f:
    f.write(f"{datetime.utcnow().isoformat()} | Available: {available} | Sold: {sold}\n")

print(f"Logged: {available} available, {sold} sold")port requests
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

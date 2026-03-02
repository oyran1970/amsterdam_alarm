import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from twilio.rest import Client
import subprocess

# --- KONFIGURASJON ---
LOG_PATH = "log/ticket_checker.log"
GH_PAGES_BRANCH = "gh-pages"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")  # sett i Actions secrets
REPO = "oyran1970/amsterdam_alarm"

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.environ.get("TWILIO_FROM")  # Twilio-nummer
TWILIO_TO = os.environ.get("TWILIO_TO")      # Ditt nummer

TARGET_URL = "https://atleta.cc/e/nhIVWn50Rcez/resale"

# --- HENT DATA FRA NETT ---
try:
    r = requests.get(TARGET_URL)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    # Eksempel: finn available og sold, juster etter nettsiden
    available_text = soup.find("span", class_="available").text
    sold_text = soup.find("span", class_="sold").text
    available = int(available_text.strip())
    sold = int(sold_text.strip())
except Exception as e:
    print("Feil ved henting/parsing:", e)
    available = sold = 0

# --- LOGGING TIL FIL ---
os.makedirs("log", exist_ok=True)
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
line = f"{timestamp}, Available: {available}, Sold: {sold}\n"

with open(LOG_PATH, "a") as f:
    f.write(line)

print(f"Logged: {available} available, {sold} sold")

# --- SEND SMS HVIS LEDIG ---
if available > 0 and all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM, TWILIO_TO]):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = f"Billetter tilgjengelig! Available: {available}, Sold: {sold}"
        client.messages.create(body=message, from_=TWILIO_FROM, to=TWILIO_TO)
        print("SMS sendt!")
    except Exception as e:
        print("Feil ved sending av SMS:", e)

# --- PUSH TIL GH-PAGES FOR OPPDATERING AV LOGG ---
try:
    subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"], check=True)
    subprocess.run(["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)
    subprocess.run(["git", "checkout", GH_PAGES_BRANCH], check=True)
    subprocess.run(["git", "add", LOG_PATH], check=True)
    subprocess.run(["git", "commit", "-m", f"Update ticket log {timestamp}"], check=True)
    subprocess.run([
        "git", "push",
        f"https://x-access-token:{GITHUB_TOKEN}@github.com/{REPO}.git",
        GH_PAGES_BRANCH
    ], check=True)
    print("Logg pushet til GitHub Pages!")
except subprocess.CalledProcessError as e:
    print("Feil ved push til GitHub Pages:", e)

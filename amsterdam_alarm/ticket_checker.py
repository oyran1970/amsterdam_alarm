import os
import logging
from datetime import datetime
import random  # Kun til testing, fjern når du har egen sjekk

# --- Oppsett av logg ---
log_dir = "amsterdam_alarm"
os.makedirs(log_dir, exist_ok=True)  # Sørg for at mappen finnes
log_file = os.path.join(log_dir, "ticket_checker.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# --- Dummy-funksjon for billetter ---
def sjekk_billetter():
    """
    Bytt ut denne funksjonen med faktisk kode som sjekker ledige billetter.
    Returnerer True hvis ledige billetter finnes, False ellers.
    """
    # For testing: tilfeldig resultat
    return random.choice([True, False])

# --- Hovedfunksjon ---
def main():
    try:
        ledige = sjekk_billetter()
        if ledige:
            logging.info("Ledige billetter funnet!")
            # Her kan du sende SMS via Twilio
        else:
            logging.info("Ingen ledige billetter denne gangen.")
    except Exception as e:
        logging.error(f"Feil under kjøring: {e}")

if __name__ == "__main__":
    main()

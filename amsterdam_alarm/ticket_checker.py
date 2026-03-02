import os
import logging
from datetime import datetime
import random  # Til testing, fjern når du bruker egen sjekk

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
    Returnerer antall ledige billetter (0 = ingen ledige).
    """
    # For testing: tilfeldig antall
    return random.choice([0, 0, 1, 2, 3])  # Flere 0 for å teste "ingen billetter"

# --- Hovedfunksjon ---
def main():
    try:
        antall_ledige = sjekk_billetter()
        if antall_ledige > 0:
            logging.info(f"Ledige billetter funnet: {antall_ledige} stk")
            # Her kan du sende SMS via Twilio
        else:
            logging.info("Ingen ledige billetter denne gangen.")
    except Exception as e:
        logging.error(f"Feil under kjøring: {e}")

if __name__ == "__main__":
    main()

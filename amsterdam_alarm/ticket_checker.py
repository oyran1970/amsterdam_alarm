import os
from datetime import datetime
from twilio.rest import Client

# ===============================
# Konfigurasjon fra miljøvariabler
# ===============================
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")
YOUR_NUMBER = os.environ.get("YOUR_NUMBER")

# ===============================
# Funksjon som sjekker billetter
# ===============================
def sjekk_billetter():
    """
    Her legger du inn koden som sjekker siden for ledige billetter.
    Returnerer en liste med billetter (kan være tom hvis ingen ledige).
    """
    # Eksempel: ingen billetter tilgjengelig
    billetter = []  
    # Hvis du finner ledige billetter, f.eks:
    # billetter = ["Billett 1", "Billett 2"]
    return billetter

# ===============================
# Funksjon for logging
# ===============================
def logg_melding(melding):
    loggfil = "check_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linje = f"{timestamp} - {melding}\n"
    print(linje, end="")  # vis i Actions log
    with open(loggfil, "a") as f:
        f.write(linje)

# ===============================
# Hovedprogram
# ===============================
def main():
    billetter = sjekk_billetter()
    
    if billetter:
        melding = f"Fant {len(billetter)} billetter: {', '.join(billetter)}"
        logg_melding(melding)
        
        if all([TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER, YOUR_NUMBER]):
            try:
                client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
                sms = client.messages.create(
                    body=melding,
                    from_=TWILIO_NUMBER,
                    to=YOUR_NUMBER
                )
                logg_melding(f"SMS sendt: {sms.sid}")
            except Exception as e:
                logg_melding(f"Feil ved sending av SMS: {e}")
        else:
            logg_melding("Twilio secrets mangler, SMS ikke sendt")
    else:
        logg_melding("Ingen ledige billetter funnet denne gangen.")

if __name__ == "__main__":
    main()

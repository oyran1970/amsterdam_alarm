name: Check Tickets

on:
  schedule:
    - cron: "*/5 * * * *"  # kjør hvert 5. minutt
  workflow_dispatch:       # gjør det mulig å starte manuelt

jobs:
  check:
    runs-on: ubuntu-latest

    steps:
      # Sjekk ut repo
      - uses: actions/checkout@v4

      # Sett opp Python
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      # Installer dependencies
      - run: pip install -r requirements.txt

      # Installer Playwright-browsere
      - name: Install Playwright browsers
        run: python -m playwright install

      # Installer nødvendige Ubuntu-dependencies
      - name: Install Playwright system dependencies
        run: sudo apt-get update && sudo apt-get install -y \
          libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
          libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0

      # Kjør ticket_checker.py
      - name: Run ticket checker
        run: /usr/bin/python3 amsterdam_alarm/ticket_checker.py
        env:
          TWILIO_SID: ${{ secrets.TWILIO_SID }}
          TWILIO_AUTH_TOKEN: ${{ secrets.TWILIO_AUTH_TOKEN }}
          TWILIO_NUMBER: ${{ secrets.TWILIO_NUMBER }}
          YOUR_NUMBER: ${{ secrets.YOUR_NUMBER }}

#!/usr/bin/env bash

# Lesen Sie die Werte aus der Add-on-Konfiguration (options.json)
CONFIG_PATH=/data/options.json
YOUR_WIFI_SSID=$(jq --raw-output '.your_wifi_ssid' "$CONFIG_PATH")
YOUR_WIFI_PASSWORD=$(jq --raw-output '.your_wifi_password' "$CONFIG_PATH")

# Führen Sie das Python-Skript mit den übergebenen Argumenten aus.
# -u sorgt dafür, dass die stdout-Ausgabe sofort sichtbar ist.
python3 -u /shelly_configurator.py "$YOUR_WIFI_SSID" "$YOUR_WIFI_PASSWORD"

echo "Add-on-Vorgang abgeschlossen."

# Wählen Sie ein Basis-Image. home-assistant/base bietet eine gute Grundlage.
FROM ghcr.io/home-assistant/amd64-base:latest

# Fügen Sie die erforderlichen Pakete hinzu.
# python3-dbus ist für die D-Bus-Kommunikation erforderlich.
# jq wird im run.sh-Skript zum Parsen der Konfiguration verwendet.
RUN apt-get update && \
    apt-get install -y python3-dbus python3-pip jq && \
    apt-get clean

# Installieren Sie die Python-Abhängigkeiten.
RUN pip3 install pydbus requests

# Kopieren Sie Ihr Python-Skript und das Start-Skript in den Container.
COPY shelly_configurator.py /
COPY run.sh /

# Setzen Sie die Berechtigungen für das Ausführen der Skripte.
RUN chmod a+x /run.sh

# Befehl zum Ausführen beim Start des Containers.
CMD [ "/run.sh" ]

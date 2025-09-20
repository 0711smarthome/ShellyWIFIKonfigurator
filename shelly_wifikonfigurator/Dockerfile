# Verwenden Sie ein schlankes Python-Image als Basis
FROM python:3.11-slim

# Fügen Sie die erforderlichen Pakete hinzu (jq für das run.sh-Skript)
RUN apt-get update && \
    apt-get install -y jq libdbus-1-dev && \
    apt-get clean

# Installieren Sie die Python-Abhängigkeiten
RUN pip install pydbus requests

# Kopieren Sie Ihr Python-Skript und das Start-Skript in den Container
COPY shelly_configurator.py /
COPY run.sh /

# Setzen Sie die Berechtigungen für das Ausführen der Skripte
RUN chmod a+x /run.sh

# Befehl zum Ausführen beim Start des Containers
CMD [ "/run.sh" ]

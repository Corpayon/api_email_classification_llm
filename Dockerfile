# Verwende ein offizielles Python-Image als Basis
FROM python:3.8-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die aktuellen Dateien in das Container-Verzeichnis /app
COPY . /app

# Installiere benötigte Python-Pakete aus der Datei requirements.txt
# Stelle sicher, dass du eine requirements.txt-Datei mit allen benötigten Paketen hast
RUN pip install --no-cache-dir -r requirements.in

# Der Befehl, der ausgeführt wird, wenn der Container startet
CMD ["python", "./api_interface.py"]
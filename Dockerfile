# Gebruik een officiële Python-runtime als basisafbeelding
FROM python:3.12-slim

# Stel de werkdirectory in
WORKDIR /app

# Kopieer de huidige directory inhoud naar de werkdirectory in de container
COPY . /app

# Installeer afhankelijkheden
RUN pip install --no-cache-dir -r requirements.txt

# Stel Flask in om op poort 4545 te draaien
EXPOSE 4545

# Commando om de applicatie te starten
CMD ["python", "main.py"]

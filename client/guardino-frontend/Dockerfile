# Basis-Image mit Node
FROM node:20-alpine

# Arbeitsverzeichnis im Container
WORKDIR /app

RUN npm install -g @angular/cli

# Nur package-Dateien zuerst für besseren Cache
COPY package*.json ./


RUN npm install

# Restlichen Code kopieren
COPY . .

# Angular Dev Server Port
EXPOSE 4200

# Standard-Command: Angular Dev Server starten
# Voraussetzung: @angular/cli ist als devDependency installiert
CMD ["npm", "run", "start"]

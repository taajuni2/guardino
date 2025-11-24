# Basis-Image mit Node
FROM node:20-alpine

# Arbeitsverzeichnis im Container
WORKDIR /app

# Nur package-Dateien zuerst für besseren Cache
COPY package*.json ./

# Dependencies installieren
RUN npm ci

# Restlichen Code kopieren
COPY . .

# Angular Dev Server Port
EXPOSE 4200

# Standard-Command: Angular Dev Server starten
# Voraussetzung: @angular/cli ist als devDependency installiert
CMD ["npx", "ng", "serve", "--host", "0.0.0.0", "--port", "4200"]

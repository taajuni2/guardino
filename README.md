# Guardino – Lightweight Ransomware Detection System
Guardino ist ein schlankes, containerisiertes Ransomware Detection System für kleine und mittlere Unternehmen.
Es besteht aus einem zentralen Client-System (inkl. Webinterface) und verteilten Agents, die auf Hosts laufen und verdächtige File-Operationen überwachen.


## Systemarchitektur
Das Guardino-System besteht aus zwei Hauptkomponenten:
1. Client (Zentrales System)
   - Frontend (Angular)
   - Backend (Python/FastAPI)
   - Datenbank (PostgreSQL)
   - Kafka-Broker für Event-Ingestion vom Agent
<br>
<br>
2. Agent
   - Lightweight Detection Engine
   - Läuft auf separaten Hosts
   - Sendet Events über Kafka an das zentrale Backend
   - Konfigurierbar (Blacklist, Extensions, Thresholds)

___

## Installation - Voraussetzungen 

- Docker installieren -> `sudo apt install docker.io`
- Docker-compose installieren -> `sudo apt install docker-compose`





### Troubleshooting - Fehlerbehbung

PostgreSQL debugging
Frontend Config 
Backend Config 
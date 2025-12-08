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

2. Agent
   - Lightweight Detection Engine
   - Läuft auf separaten Hosts
   - Sendet Events über Kafka an das zentrale Backend
   - Konfigurierbar (Blacklist, Extensions, Thresholds)



## Installation & Setup
### Voraussetzungen
- Docker installieren -> `sudo apt install docker.io`
- Docker-compose installieren -> `sudo apt install docker-compose`

Zudem muss sichergestellt werden das keine Firewall Rule den Traffic zwischen Client und Agent behindert. 

### Installation Client 
1. Navigiere zum Guardino Project Root Ordner 
2. Konfiguration direkt im Docker-Compose file anpassen falls nötig (ENV-Vars)
3. Deployment des Client's starten mit `docker-compose up` (falls error -> sudo verwenden)


### Installation Agent
1. Navigiere zum Agent Ordner unter Guardino -> Agent
2. Konfigurationsdatei im Guardino/Agent/config/agent_config.yaml anpassen und konfigurieren 
3. Sicherstellen das alle dependencies in einem Virtual Environment installiert werden (global ist nicht empfohlen)
4. Starte den Agent mit dem Befehl `python3 main.py`




### Troubleshooting - Fehlerbehbung

PostgreSQL debugging <br>

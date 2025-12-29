# Guardino Agent 
Der Guardino Agent ist ein leichtgewichtiger Host-basierter Detection Agent zur Erkennung von verdächtigen Dateiaktivitäten (z. B. Ransomware-typisches Verhalten).
Der Agent läuft direkt auf dem Zielsystem und sendet Events an eine zentrale Kafka-Infrastruktur.


### Kernkomponenten
**File Monitor**
- Überwacht konfigurierte Verzeichnisse 
- Erkennt Datei-Erstellung -Änderung 
- Blacklist-Mechanismus zum Ausschluss kritischer Pfade

**Detection Engine**
- Massenhafte Datei-Erstellung in kurzen Zeitfenstern
- Dateien mit hoher Entropie (Hinweis auf Verschlüsselung)
- Cooldown-Mechanismus zur Vermeidung von Alert-Spam

**Event System**
- Strukturierte Detection-Events
- Asynchroner Versand
- Kafka als Transport-Layer


**Agent Lifecycle**
- Automatische Registrierung beim ersten Start
- Persistente Agent-ID pro Host
- Regelmäßige Heartbeats



## Installation






### Komponenten Übersicht
```
+------------------+
|   Guardino Agent |
|------------------|
|  File Monitoring |
|  Detection Engine|
|  Event Producer  |
+--------+---------+
         |
         v
     Kafka Broker
         |
         v
+------------------+
| Central Backend  |
|  API + Web GUI   |
+------------------+
```



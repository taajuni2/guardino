# Guardino-Backend
Das Guardino Backend ist die zentrale Steuereinheit des Systems.
Es empfängt Events von Agents, verarbeitet diese, speichert sie persistent und stellt eine API für das Frontend bereit.

### Aufgaben des Backends 
- Entgegennahme von Agent-Events über Kafka
- Verarbeitung und Persistierung von Detection- und Lifecycle-Events
- Verwaltung von Agent-Status und Heartbeats
- Bereitstellung einer REST-API & Websocket für das Web-Frontend


### Bestandteile 
Folgende Komponenten sind Bestandteile vom Backend: 
- REST API (Python / Flask)
- Kafka Consumer (Events, Lifecycle)
- PostgreSQL Datenbank
- Interne Event- und Agent-Logik

Der Kafka-Broker wird als Teil des Backend-Stacks betrieben.



### Installation
Erfolgt über docker-compose.yml im Guardino Ordner.
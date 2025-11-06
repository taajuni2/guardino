# Guardino-System

Guardino ist ein Lightweight Ransomware Detection Tool für Klein- und Mittelunternehmen. <br>

**Das Guardino System besteht aus folgenden Komponenten:**
* Client (Frontend, Backend, DB, KafkaBroker)
* Agent (Ransomware Detection)



### Installation
alembic upgrade head
alembic revision --autogenerate -m "Added event table"
uvicorn app.main:app --reload


#### Local 



#### Non-Local

### Config parameters 




### Troubleshooting 



#### Manual DB access:

1. Connect to Container 

``
 docker exec -it guardino-db /bin/bash``<br>
2. Access Postgres DB <br> 

\pset expanded on -> für bessere Lesbarkeit <br>

``psql -U postgres guardino``SELE

UPDATE alembic_version SET version_num = '83fcfc501973';
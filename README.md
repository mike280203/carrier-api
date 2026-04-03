# Carrier API

FastAPI-Projekt fuer die SWE-Abgabe mit PostgreSQL, spaeter GraphQL und Keycloak.

## Aktueller Stand

- PostgreSQL-Setup fuer `carrier` ist vorbereitet
- FastAPI-App startet
- Basis-Endpunkte:
  - `/`
  - `/health`
  - `/rest/carriers`
- GraphQL und Keycloak werden spaeter wieder integriert

## Voraussetzungen

- Docker Desktop
- Python / `uv`
- Git

## Projekt starten

### 1. Repository klonen

```powershell
git clone <REPO-URL>
cd carrier-api
```

### 2. Python-Abhaengigkeiten installieren

```powershell
uv sync --all-groups
```

## PostgreSQL-Setup

Die Docker-Volumes sind lokal auf jedem Rechner separat. Nach dem Pull aus GitHub
muss jede Person das Postgres-Setup einmal selbst ausfuehren.

### 1. In den PostgreSQL-Ordner wechseln

```powershell
cd extras\compose\postgres
```

### 2. Docker-Volumes anlegen

```powershell
docker volume create carrier_pg_data
docker volume create carrier_pg_tablespace
docker volume create carrier_pg_init
```

### 3. Init-Dateien in die Docker-Volumes kopieren

```powershell
docker run -v carrier_pg_init:/init -v carrier_pg_tablespace:/tablespace -v ${PWD}\init:/tmp/init:ro --rm -it -u 0 --entrypoint "" dhi.io/postgres:18.3-debian13 /bin/bash
```

Dann im Container:

```bash
cp -r /tmp/init/* /init
mkdir /tablespace/carrier
chown -R postgres:postgres /init /tablespace
chmod 400 /init/*/sql/* /init/tls/*
exit
```

### 4. PostgreSQL beim ersten Mal ohne TLS initialisieren

In `extras/compose/postgres/compose.yml` die Zeile

```yml
command: ["-c", "ssl=on"]
```

temporaer auskommentieren.

Dann starten:

```powershell
docker compose up db
```

### 5. TLS-Dateien ins Postgres-Datenverzeichnis kopieren

In einer zweiten PowerShell:

```powershell
cd extras\compose\postgres
docker compose exec db bash -c "cp /init/tls/* /var/lib/postgresql/18/data"
docker compose down
```

### 6. TLS wieder einschalten

In `extras/compose/postgres/compose.yml` die Zeile

```yml
command: ["-c", "ssl=on"]
```

wieder einkommentieren.

Dann PostgreSQL erneut starten:

```powershell
docker compose up db
```

### 7. Datenbank und Schema anlegen

```powershell
docker compose exec db bash
psql --dbname=postgres --username=postgres --file=/init/carrier/sql/create-db.sql
psql --dbname=carrier --username=carrier --file=/init/carrier/sql/create-schema.sql
exit
```

Optional in `psql`:

```sql
\pset pager off
\l
\c carrier
\dn
\dt
```

## Tabellen anlegen

Die Tabellenstruktur liegt in:

- `src/carrier/config/resources/postgresql/create.sql`

Falls `create.sql` noch nicht unter `extras/compose/postgres/init/carrier/sql` liegt,
zuerst kopieren:

```powershell
Copy-Item ..\..\..\src\carrier\config\resources\postgresql\create.sql .\init\carrier\sql\create.sql
```

Danach die Datei auch in das Docker-Volume `carrier_pg_init` kopieren:

```powershell
docker run -v carrier_pg_init:/init -v ${PWD}\init:/tmp/init:ro --rm -it -u 0 --entrypoint "" dhi.io/postgres:18.3-debian13 /bin/bash
```

Im Container:

```bash
cp /tmp/init/carrier/sql/create.sql /init/carrier/sql/create.sql
chown postgres:postgres /init/carrier/sql/create.sql
chmod 400 /init/carrier/sql/create.sql
exit
```

Dann im laufenden DB-Container ausfuehren:

```powershell
docker compose exec db bash
psql --dbname=carrier --username=carrier --file=/init/carrier/sql/create.sql
exit
```

## App-Konfiguration

Die zentrale Konfiguration liegt in:

- `src/carrier/config/resources/app.toml`

Wichtiger DB-Block:

```toml
[db]
# username = "carrier"
# name = "carrier"
password = "p"
password-admin = "p"
host = "localhost"
log-statements = true
```

Hinweis:
- `username` und `name` sind aktuell auskommentiert
- das funktioniert, weil im Code bereits `carrier` als Default gesetzt ist
- fuer mehr Klarheit koennen diese beiden Werte explizit einkommentiert werden

## App starten

Im Projektroot:

```powershell
cd C:\Users\mikes\Desktop\carrier-api
uv run python -m carrier
```

## Testen

Im Browser:

- `https://127.0.0.1:8000/`
- `https://127.0.0.1:8000/health`
- `https://127.0.0.1:8000/rest/carriers`

## Wichtige Hinweise fuer das Team

- Das Beispielprojekt `patient` bleibt unangetastet
- Die Docker-Volumes fuer dieses Projekt heissen:
  - `carrier_pg_data`
  - `carrier_pg_tablespace`
  - `carrier_pg_init`
- Diese Volumes sind lokal und werden nicht ueber GitHub geteilt
- Jede Person im Team muss das Docker-/DB-Setup einmal selbst ausfuehren

## Naechste Schritte im Projekt

Empfohlene Reihenfolge:

1. REST-Schnittstellen sauber fertig bauen
2. Service- und Repository-Logik erweitern
3. Tests schreiben
4. GraphQL integrieren
5. Keycloak integrieren

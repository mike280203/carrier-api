# Carrier API

FastAPI-Projekt fuer die Verwaltung von Carriern mit PostgreSQL, SQLAlchemy und Strawberry GraphQL.

## Projektstatus

Der aktuelle Stand im Repository umfasst bereits die fachliche Basis fuer Lesen, Anlegen, Aktualisieren und Loeschen von Carriern. Neben der REST-Schnittstelle ist auch eine GraphQL-Schnittstelle eingebunden. Zusaetzlich sind Monitoring, TLS-Start, Konfigurationsverwaltung und optionale Dev-Helfer fuer Datenbank- und Keycloak-Befuellung vorhanden.

## Aktuelle Funktionen

- REST-API fuer Carrier unter `/rest/carriers`
- GraphQL-Endpunkt unter `/graphql`
- CRUD fuer Carrier:
  - `GET /rest/carriers/{id}`
  - `GET /rest/carriers`
  - `POST /rest/carriers`
  - `PUT /rest/carriers/{id}`
  - `DELETE /rest/carriers/{id}`
- Filter in der REST-Suche ueber `name`, `nation` und `carrier_type`
- Paging in der REST-Suche ueber `page` und `size`
- ETag-Unterstuetzung bei `GET /rest/carriers/{id}`
- Optimistic Locking bei `PUT /rest/carriers/{id}` ueber `If-Match`
- Problem-Details-Responses fuer typische Fehlerfaelle
- Prometheus-Metriken
- GZip-Middleware und einfache Security-Header
- Optionales Dev-Populate fuer Datenbank und Keycloak
- SMTP-Mailer als vorbereitete Service-Komponente

## Datenmodell

Ein Carrier besteht aktuell aus:

- `id`
- `version`
- `name`
- `nation`
- `carrier_type`
- `commandcenter`
- `aircrafts`

Zum `commandcenter` gehoeren:

- `code_name`
- `security_level`

Zu `aircrafts` gehoeren pro Eintrag:

- `model`
- `manufacturer`

## REST-Endpunkte

### Basis-Endpunkte

- `GET /`
- `GET /health`
- `GET /metrics`

### Carrier lesen

- `GET /rest/carriers/{id}`
  - liefert einen Carrier per ID
  - setzt einen `ETag`-Header mit der aktuellen Version
  - unterstuetzt `If-None-Match`
- `GET /rest/carriers`
  - liefert eine paginierte Liste
  - unterstuetzt die Suchparameter `name`, `nation`, `carrier_type`
  - unterstuetzt `page` und `size`

### Carrier schreiben

- `POST /rest/carriers`
  - legt einen Carrier inklusive `commandcenter` und `aircrafts` an
  - liefert `201 Created` und einen `Location`-Header
- `PUT /rest/carriers/{id}`
  - aktualisiert vorhandene Carrier-Daten
  - erwartet einen gueltigen `If-Match`-Header mit der Versionsnummer
  - liefert bei Erfolg `204 No Content` und einen neuen `ETag`
- `DELETE /rest/carriers/{id}`
  - loescht einen Carrier per ID

## GraphQL

Die GraphQL-Schnittstelle ist unter `/graphql` eingebunden.

Aktuell vorhanden:

- Query `carrier(carrierId)`
- Query `carriers(suchparameter)`
- Mutation `create(carrierInput)`

Die Suche unterstuetzt auch in GraphQL:

- `name`
- `nation`
- `carrier_type`

## Fehlerverhalten

Die API verwendet Problem Details (`application/problem+json`) fuer fachliche und technische Fehlerfaelle, unter anderem fuer:

- `404 Not Found`
- `409 Conflict`
- `412 Precondition Failed`
- `428 Precondition Required`
- `422 Unprocessable Content`

## Technologie-Stack

- Python 3.14
- FastAPI
- Uvicorn
- SQLAlchemy
- PostgreSQL
- Strawberry GraphQL
- Pydantic v2
- Loguru
- Prometheus FastAPI Instrumentator
- `uv` fuer Dependency-Management und Start

## Voraussetzungen

- Python 3.14+
- `uv`
- Docker Desktop
- PostgreSQL via Docker Compose

## Projekt lokal starten

### 1. Repository klonen

```powershell
git clone <REPO-URL>
cd carrier-api
```

### 2. Abhaengigkeiten installieren

```powershell
uv sync --all-groups
```

### 3. Konfiguration pruefen

Die zentrale Konfiguration liegt in `src/carrier/config/resources/app.toml`.

Wichtige Bereiche:

- `server`
- `tls`
- `db`
- `mail`
- `graphql`
- `keycloak`
- `dev`

### 4. PostgreSQL starten

Die Compose-Dateien liegen unter `extras/compose/postgres`.

Beim ersten Setup muessen die benoetigten Docker-Volumes lokal angelegt werden:

```powershell
docker volume create carrier_pg_data
docker volume create carrier_pg_tablespace
docker volume create carrier_pg_init
```

Danach kann das DB-Setup ueber die Dateien in `extras/compose/postgres` und `src/carrier/config/resources/postgresql` initialisiert werden.

### 5. Anwendung starten

```powershell
uv run carrier
```

Die Anwendung startet standardmaessig mit TLS ueber Uvicorn.

## Wichtige URLs lokal

- `https://127.0.0.1:8000/`
- `https://127.0.0.1:8000/health`
- `https://127.0.0.1:8000/docs`
- `https://127.0.0.1:8000/redoc`
- `https://127.0.0.1:8000/graphql`
- `https://127.0.0.1:8000/metrics`

## Beispiel fuer einen neuen Carrier

```json
{
  "name": "USS Gerald R. Ford",
  "nation": "United States",
  "carrier_type": "AIRCRAFT_CARRIER",
  "commandcenter": {
    "code_name": "Ford Command",
    "security_level": 5
  },
  "aircrafts": [
    {
      "model": "F-35C",
      "manufacturer": "Lockheed Martin"
    },
    {
      "model": "E-2D Hawkeye",
      "manufacturer": "Northrop Grumman"
    }
  ]
}
```

## Entwicklung und Hilfswerkzeuge

- Bruno-Collections fuer Requests liegen unter `extras/bruno`
- Compose-Setups fuer lokale Infrastruktur liegen unter `extras/compose`
- Dev-Routen fuer Datenbank- und Keycloak-Befuellung werden nur aktiviert, wenn die entsprechenden Flags in `app.toml` gesetzt sind:
  - `POST /dev/db/populate`
  - `POST /dev/keycloak/populate`

## Aktuell vorbereitet, aber noch nicht voll integriert

- Keycloak-Konfiguration und Populate-Logik sind vorhanden, die REST-Routen erzwingen derzeit aber noch keine Authentifizierung.
- Der Mailer ist implementiert, wird beim Anlegen eines Carriers aktuell noch nicht aktiv aufgerufen.
- Excel- und weitere Zusatzkonfigurationen sind im Projekt angelegt, spielen aber im aktuellen API-Flow noch keine zentrale Rolle.

## Hinweise fuer das Team

- Docker-Volumes sind lokal und werden nicht ueber Git geteilt.
- Das Datenbank-Setup muss auf jeder Maschine einmal lokal durchgefuehrt werden.
- Fuer einen sauberen lokalen Start sollten TLS-Dateien und DB-Konfiguration zur jeweiligen Umgebung passen.

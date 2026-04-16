# Carrier API

Carrier API ist ein FastAPI-Server zur Verwaltung von Carriern mit PostgreSQL als Datenbank. Die Anwendung stellt eine REST-Schnittstelle und eine GraphQL-Schnittstelle bereit und unterstützt Lesen, Anlegen, Aktualisieren und Löschen von Carriern inklusive zugehörigem Command Center und Aircrafts.

## Funktionen

- REST-API unter `/rest/carriers`
- GraphQL-API unter `/graphql`
- CRUD für Carrier
- Suche über `name`, `nation` und `carrier_type`
- Pagination über `page` und `size`
- Versionierung mit `ETag`, `If-None-Match` und `If-Match`
- Keycloak-basierte Authentifizierung und rollenbasierte Autorisierung
- Prometheus-Metriken und Health-Endpoint

## Sicherheitsmodell

- `admin` darf lesen und schreiben
- `user` darf lesen

## Wichtige Endpunkte

- `GET /health`
- `GET /metrics`
- `GET /rest/carriers`
- `GET /rest/carriers/{id}`
- `POST /rest/carriers`
- `PUT /rest/carriers/{id}`
- `DELETE /rest/carriers/{id}`
- `POST /graphql`

## Technologie-Stack

- Python 3.14
- FastAPI
- SQLAlchemy
- PostgreSQL
- Strawberry GraphQL
- Keycloak
- Uvicorn
- `uv`

## Projektstruktur

- [src/carrier/router](src/carrier/router) REST-Router
- [src/carrier/graphql_api](src/carrier/graphql_api) GraphQL-Schema
- [src/carrier/service](src/carrier/service) Geschäftslogik
- [src/carrier/repository](src/carrier/repository) Datenzugriff
- [src/carrier/security](src/carrier/security) Keycloak- und Rollenlogik
- [extras/compose](extras/compose) Docker-Compose-Setups

## Start

Lokal:

```powershell
uv sync --all-groups
uv run carrier
```

Mit Docker:

```powershell
docker build -t juergenzimmermann/carrier:2026.4.1-hardened .
Set-Location extras/compose/carrier
docker compose up
```

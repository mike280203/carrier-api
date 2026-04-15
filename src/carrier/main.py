"""Haupteinstiegspunkt für den App-Server."""

from fastapi import FastAPI

app = FastAPI(title="Aircraft Carrier API")


@app.get("/")
def root():
    """Root-Pfad für einfache Verfügbarkeitsprüfung."""
    return {"message": "Carrier API is running"}

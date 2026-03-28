from fastapi import FastAPI

app = FastAPI(title="Aircraft Carrier API")


@app.get("/")
def root():
    return {"message": "Carrier API is running"}
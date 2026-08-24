from fastapi import FastAPI

app = FastAPI(title="WHOOP + Garmin Health Hub API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

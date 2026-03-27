from fastapi import FastAPI

app = FastAPI(
    title="Vendor Management API",
    description="REST API for tracking and auditing vendor relationships.",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}

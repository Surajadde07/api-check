from fastapi import FastAPI, BackgroundTasks
from ingestion import enqueue_ingestion, get_ingestion_status
from models import IngestionRequest
from processor import batch_worker
import asyncio

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(batch_worker())

@app.post("/ingest")
async def ingest(data: IngestionRequest):
    ingestion_id = enqueue_ingestion(data.ids, data.priority)
    return {"ingestion_id": ingestion_id}

@app.get("/status/{ingestion_id}")
async def status(ingestion_id: str):
    status = get_ingestion_status(ingestion_id)
    if not status:
        return {"error": "Invalid ingestion_id"}
    return status

@app.get("/")
async def root():
    return {"message": "API is running! Go to /docs for API docs."}

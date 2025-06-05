# Data Ingestion API

## Features
- Priority-based asynchronous ingestion
- Rate-limited (1 batch per 5 seconds)
- Status tracking

## Tech
- FastAPI
- asyncio
- In-memory queue

## Run Locally

```bash
git clone <repo>
cd data_ingestion_api
pip install -r requirements.txt
uvicorn main:app --reload

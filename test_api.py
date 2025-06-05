import pytest
from fastapi.testclient import TestClient
from main import app
import time

client = TestClient(app)

def test_ingest_and_status():
    res = client.post("/ingest", json={"ids": [1, 2, 3, 4, 5], "priority": "MEDIUM"})
    assert res.status_code == 200
    ingestion_id = res.json()["ingestion_id"]

    res2 = client.post("/ingest", json={"ids": [6, 7, 8, 9], "priority": "HIGH"})
    assert res2.status_code == 200
    high_id = res2.json()["ingestion_id"]

    time.sleep(1)
    res3 = client.get(f"/status/{high_id}")
    assert res3.status_code == 200
    assert "batches" in res3.json()

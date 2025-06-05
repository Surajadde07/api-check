from uuid import uuid4
from datetime import datetime
from database import ingestions, priority_queue, db_lock

BATCH_SIZE = 3

def enqueue_ingestion(ids, priority) -> str:
    ingestion_id = str(uuid4())
    now = datetime.utcnow()
    batches = []

    for i in range(0, len(ids), BATCH_SIZE):
        batch = {
            "batch_id": str(uuid4()),
            "ids": ids[i:i+BATCH_SIZE],
            "status": "yet_to_start"
        }
        batches.append(batch)

        priority_queue[priority].append({
            "ingestion_id": ingestion_id,
            "batch": batch,
            "created_time": now,
            "priority": priority
        })

    with db_lock:
        ingestions[ingestion_id] = {
            "status": "yet_to_start",
            "priority": priority,
            "created_time": now,
            "batches": batches
        }

    return ingestion_id

def get_ingestion_status(ingestion_id):
    if ingestion_id not in ingestions:
        return None

    ingestion = ingestions[ingestion_id]
    batch_statuses = [b['status'] for b in ingestion['batches']]
    if all(s == "yet_to_start" for s in batch_statuses):
        overall = "yet_to_start"
    elif all(s == "completed" for s in batch_statuses):
        overall = "completed"
    else:
        overall = "triggered"

    return {
        "ingestion_id": ingestion_id,
        "status": overall,
        "batches": ingestion['batches']
    }

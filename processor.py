import asyncio
from database import priority_queue, ingestions, db_lock
import time

PRIORITY_ORDER = ['HIGH', 'MEDIUM', 'LOW']

async def fetch_data(id_):
    await asyncio.sleep(1)  # simulate API delay
    return {"id": id_, "data": "processed"}

async def process_batch(ingestion_id, batch):
    batch['status'] = 'triggered'
    with db_lock:
        ingestion = ingestions[ingestion_id]
    await asyncio.gather(*[fetch_data(i) for i in batch['ids']])
    batch['status'] = 'completed'

async def batch_worker():
    while True:
        found_batch = None
        for priority in PRIORITY_ORDER:
            if priority_queue[priority]:
                found_batch = priority_queue[priority].pop(0)
                break

        if found_batch:
            ingestion_id = found_batch['ingestion_id']
            batch = found_batch['batch']
            await process_batch(ingestion_id, batch)
        await asyncio.sleep(5)  # rate limit: 1 batch per 5 seconds

from collections import defaultdict
from typing import Dict, List
from threading import Lock

db_lock = Lock()

# Example: {ingestion_id: {status, priority, created_time, batches: [batch_dicts]}}
ingestions: Dict[str, dict] = {}

# Queue by priority
priority_queue: Dict[str, List[dict]] = {
    "HIGH": [],
    "MEDIUM": [],
    "LOW": []
}

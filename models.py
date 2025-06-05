from pydantic import BaseModel
from typing import List, Literal

class IngestionRequest(BaseModel):
    ids: List[int]
    priority: Literal['HIGH', 'MEDIUM', 'LOW']

class BatchStatus(BaseModel):
    batch_id: str
    ids: List[int]
    status: Literal['yet_to_start', 'triggered', 'completed']

class IngestionStatus(BaseModel):
    ingestion_id: str
    status: Literal['yet_to_start', 'triggered', 'completed']
    batches: List[BatchStatus]

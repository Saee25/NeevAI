from pydantic import BaseModel
from typing import Optional

class RetrievedChunk(BaseModel):
    text: str
    source: str
    url: Optional[str] = None
    score: float

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class document(BaseModel):
    content: str
    title: str
    metadata: Optional[Dict[str, Any]] = None
    id: Optional[str] = None

        
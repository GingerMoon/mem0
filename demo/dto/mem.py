from typing import List, Optional

from pydantic import BaseModel


class AddPayload(BaseModel):
    messages: List[dict[str, str]]
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    run_id: Optional[str] = None
    metadata: Optional[dict] = None
    filters: Optional[dict] = None
    prompt: Optional[str] = None
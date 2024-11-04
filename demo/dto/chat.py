from typing import Optional

from pydantic import BaseModel


class ChatPayload(BaseModel):
    system_prompt: Optional[str] = None
    query: str
    user_id: str
    run_id: Optional[str] = None
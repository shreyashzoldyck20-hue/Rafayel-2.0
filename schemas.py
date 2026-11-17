from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)
    conversation_id: str | None = None

class ChatResponse(BaseModel):
    conversation_id: str
    reply: str
    provider: str
    emotional_tone: str

class MemoryRequest(BaseModel):
    content: str = Field(min_length=1, max_length=2000)

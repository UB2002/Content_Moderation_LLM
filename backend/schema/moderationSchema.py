from pydantic import BaseModel 
from typing import Optional, Dict

class TextModeration(BaseModel):
    text: str
    email: str

class ImageModeration(BaseModel):
    email: str 

class ModerationResponse(BaseModel):
    request_id: int
    classification: str
    confidence: float
    reasoning: str
    llm_response: str




class Summary(BaseModel):
    total_request:int 
    by_classification: Dict[str, int]
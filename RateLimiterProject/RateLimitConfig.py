from pydantic import BaseModel, Field
class RateLimitConfig(BaseModel):
    limit: int
    window: int

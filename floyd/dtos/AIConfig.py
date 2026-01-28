from pydantic import BaseModel, Field

class AIConfig(BaseModel):
    diff_limit: int = Field(default=-1)
    instructions: str = Field(default="")

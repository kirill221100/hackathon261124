from pydantic import BaseModel

class DocumentResponseScheme(BaseModel):
    id: int
    name: str
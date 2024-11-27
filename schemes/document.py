from pydantic import BaseModel

class UploadDocumentResponseScheme(BaseModel):
    id: int
    name: str


class DocumentResponseScheme(BaseModel):
    id: int
    name: str
    text: str

from io import BytesIO
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemes.document import UploadDocumentResponseScheme, DocumentResponseScheme
from utils.document import upload_docs_func, get_doc_func
from db.db_setup import get_session
from typing import List

document_router = APIRouter()

@document_router.post('/upload-docs', response_model=List[UploadDocumentResponseScheme])
async def upload_docs_path(docs: List[UploadFile], session: AsyncSession = Depends(get_session)):
    return await upload_docs_func(docs, session)

@document_router.get('/doc/{doc_id}', response_model=DocumentResponseScheme)
async def get_doc(doc_id: int, session: AsyncSession = Depends(get_session)):
    return await get_doc_func(doc_id, session)

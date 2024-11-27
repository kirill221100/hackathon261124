from io import BytesIO
from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemes.document import DocumentResponseScheme
from utils.document import upload_docs_func
from db.db_setup import get_session
from typing import List

document_router = APIRouter()

@document_router.post('/upload-docs', response_model=List[DocumentResponseScheme])
async def upload_docs_path(docs: List[UploadFile], session: AsyncSession = Depends(get_session)):
    return await upload_docs_func(docs, session)

# @document_router.post('/upload-pdf', response_model=DocumentResponseScheme)
# async def upload_pdf_path(doc: UploadFile, session: AsyncSession = Depends(get_session)):
#     return await create_pdf_func(BytesIO(await doc.read()), doc.filename, session)
#
#
# @document_router.post('/upload-docx', response_model=DocumentResponseScheme)
# async def upload_docx_path(doc: UploadFile, session: AsyncSession = Depends(get_session)):
#     return await create_docx_func(BytesIO(await doc.read()), doc.filename, session)
#
# @document_router.post('/upload-txt', response_model=DocumentResponseScheme)
# async def upload_txt_path(doc: UploadFile, session: AsyncSession = Depends(get_session)):
#     # await create_txt_func(await doc.read(), doc.filename, session)
#     # return {'msg': 'File uploaded'}
#     return await create_document((await doc.read()).decode("utf-8"), doc.filename, session)

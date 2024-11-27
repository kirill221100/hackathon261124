from io import BytesIO
from pypdf import PdfReader
from docx import Document
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import List
from fastapi import UploadFile, HTTPException
from db.utils.document import create_document
from fastapi.concurrency import run_in_threadpool


def read_pdf_text(file: BytesIO):
    text = ''
    pdf = PdfReader(file)

    pages_num = len(pdf.pages)
    for page_num in range(pages_num):
        page = pdf.pages[page_num]
        text += page.extract_text() + '\n'
    return text


def read_docx_text(file: BytesIO):
    text = ''
    doc = Document(file)

    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text


async def upload_docs_func(docs: List[UploadFile], session: AsyncSession):
    res = []
    for doc in docs:
        if doc.content_type not in ('application/pdf', 'text/plain',
                                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
            raise HTTPException(400, f"Тип файла {doc.filename} не поддерживается")
    for doc in docs:
        if doc.content_type == 'application/pdf':
            res.append(await create_pdf(doc, session))
        elif doc.content_type == 'text/plain':
            res.append(await create_document((await doc.read()).decode("utf-8"), doc.filename, session))
        elif doc.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            res.append(await create_docx(doc, session))
    await session.commit()
    return res




async def create_pdf(file: UploadFile, session: AsyncSession):

    text = await run_in_threadpool(read_pdf_text, BytesIO(await file.read()))
    return await create_document(text, file.filename, session)


async def create_docx(file: UploadFile, session: AsyncSession):
    text = await run_in_threadpool(read_docx_text, BytesIO(await file.read()))
    return await create_document(text, file.filename, session)


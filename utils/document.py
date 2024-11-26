from io import BytesIO
from pypdf import PdfReader
from docx import Document
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
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


# def read_txt(file: BytesIO):



async def create_pdf_func(file: BytesIO, name: str, session: AsyncSession):
    text = await run_in_threadpool(read_pdf_text, file)
    return await create_document(text, name, session)


async def create_docx_func(file: BytesIO, name: str, session: AsyncSession):
    text = await run_in_threadpool(read_docx_text, file)
    return await create_document(text, name, session)


# async def create_txt_func(file, name: str, session: AsyncSession):
#     return await create_document(text, name, session)

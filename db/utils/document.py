from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from db.models.document import Document


async def create_document(text: str, name: str, session: AsyncSession):
    doc = Document(name=name, text=text)
    session.add(doc)
    #await session.commit()
    return doc


async def get_document_by_id(doc_id: int, session: AsyncSession):
    return (await session.execute(select(Document).filter_by(id=doc_id))).scalar_one_or_none()
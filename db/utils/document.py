from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from db.models.document import Document


async def create_document(text: str, name: str, session: AsyncSession):
    doc = Document(name=name, text=text)
    session.add(doc)
    #await session.commit()
    return doc
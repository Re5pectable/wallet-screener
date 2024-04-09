from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ...config import db_settings

engine = create_async_engine(db_settings.url)
Base = declarative_base()
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Dependency
async def get_session() -> AsyncSession: # type: ignore
    async with Session() as session:
        yield session

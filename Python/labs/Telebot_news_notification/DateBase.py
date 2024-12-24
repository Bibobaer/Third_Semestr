from Models import *
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import func

class DB:
    def __init__(self):
        try:
            self.engine = create_async_engine("sqlite+aiosqlite:///labs_news.db")

            self.connection = self.engine.connect()
            self.session = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        except Exception as e:
            print("Error. I can connect to DB", e)

    async def initialize_connection(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("connection initializated")

    async def is_news_exists(self, title: str) -> bool:
        async with self.session() as session:
            stmt = select(News.id).where(News.title == title)
            result = (await session.execute(stmt)).all()
            return bool(len(result))
        
    async def get_info(self, _id: int) -> tuple:
        async with self.session() as session:
            stml = select(News.id, News.title, News.date).where(News.id == _id)
            result = (await session.execute(stml)).first()
            return result
        
    async def get_full_news(self, _id: str) -> str:
        async with self.session() as session:
            stml = select(Full_News.name).where(Full_News.id == _id)
            result = (await session.execute(stml)).scalar()
            return result
        
    async def get_link(self, _id: str) -> str:
        async with self.session() as session:
            stml = select(News.link).where(News.id == _id)
            result = (await session.execute(stml)).scalar()
            return result

    async def max_id(self) -> int:
        async with self.session() as session:
            stml = select(func.max(News.id))
            result = await session.execute(stml)
            return result.scalar()
        
    async def add_news(self, title: str, date: str, link: str, full_news: str):
        async with self.session() as session:
            new_news = News(
                title=title,
                date=date,
                link=link
            )

            session.add(new_news)
            await session.commit()

            new_full_news = Full_News(
                name=full_news
            )

            session.add(new_full_news)
            await session.commit()


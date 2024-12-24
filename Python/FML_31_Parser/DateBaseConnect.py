from Moduls import *
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

class Connect:
    def __init__(self):
        try:
            self.engine = create_async_engine("sqlite+aiosqlite:///news.db")

            self.connection = self.engine.connect()
            self.seccion = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        except Exception as e:
            print("Ошибка при подключении к БД\n", e)

    async def initialize_connection(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("connection initializated")

    async def is_news_exists(self, title: str) -> bool:
        async with self.seccion() as seccion:
            stmt = select(News.id).where(News.title == title)
            result = (await seccion.execute(stmt)).all()
            return bool(len(result))
        
    async def is_tag_exists(self, tag: str) -> bool:
        async with self.seccion() as seccion:
            stml = select(Tag.id).where(Tag.name == tag)
            result = (await seccion.execute(stml)).all()
            return bool(len(result))
        
    async def find_id_by_tag(self, tag: str):
        async with self.seccion() as seccion:
            stml = select(Tag.id).where(Tag.name == tag)
            result = (await seccion.execute(stml)).first()
            return result
        
    async def add_news(self, title: str, date: str, descr: str, author: str, tags: list[str]):
        async with self.seccion() as seccion:
            new_news = News(
                title=title,
                date=date,
                description=descr,
                author=author
            )

            seccion.add(new_news)
            await seccion.commit()

            for tag in tags:
                if not await self.is_tag_exists(tag=tag):
                    new_tag = Tag(name=tag)
                    seccion.add(new_tag)
                    await seccion.commit()

                id_tag = await self.find_id_by_tag(tag)
                if len(id_tag) != 0:
                    seccion.add(News_Tags(id_news=new_news.id, id_tag=id_tag[0]))
                    await seccion.commit()
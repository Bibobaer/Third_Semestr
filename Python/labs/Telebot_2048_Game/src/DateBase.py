from Bases import *
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import func, update

class DataBase:
    def __init__(self):
        try:
            self.engine = create_async_engine("sqlite+aiosqlite:///game.db")
            self.connection = self.engine.connect()
            self.session = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        except Exception as e:
            print("Error. I can connect to DB", e)

    async def initialize_connection(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("connection initializated")

    async def is_exist(self, user_id: int) -> bool:
        async with self.session() as session:
            stmt = select(User.user_id).where(User.user_id == user_id)
            result = (await session.execute(stmt)).all()
            return bool(len(result))
        
    async def add_user(self, user_id: int):
        async with self.session() as session:
            new_user = User(
                user_id=user_id,
                rank=0
            )

            session.add(new_user)
            await session.commit()

    async def get_raiting(self) -> dict[int, int]:
        async with self.session() as session:
            stmt = select(User).order_by(User.rank.desc())
            result = (await session.execute(stmt))

            res_dict: dict[int, int]= {}

            rows = result.scalars().all()
            for row in rows:
                res_dict[int(row.user_id)] = int(row.rank)

            return res_dict
        
    async def get_rank(self, user_id: int) -> int:
        async with self.session() as session:
            stmt = select(User.rank).where(User.user_id == user_id)
            result = (await session.execute(stmt)).scalar()
            return result

    async def get_first_five_raiting(self) -> list[int]:
        async with self.session() as session:
            stmt = select(User).order_by(User.rank.desc())
            result = (await session.execute(stmt))

            rows = result.scalars().all()

            res_list = []

            index = 0
            for row in rows:
                if (index == 5):
                    break
                res_list.append(int(row.user_id))
                index += 1

            return res_list
        
    async def update_rank(self, user_id: int, new_rank: int):
        async with self.session() as session:
            stmt = update(User).where(User.user_id == user_id).values(rank=new_rank)
            await session.execute(stmt)
            await session.commit()
        
    async def is_top_one(self, rank: int) -> (bool | None):
        async with self.session() as session:
            stmt = select(func.max(User.rank))
            result = (await session.execute(stmt)).scalar()
            if (result is None):
                return None
            return True if rank > result else False
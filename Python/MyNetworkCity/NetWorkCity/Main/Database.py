from Main.Bases import *
from sqlalchemy.future import select
from sqlalchemy import update, and_, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

class DataBase:
    def __init__(self):
        try:
            self.engine = create_async_engine("sqlite+aiosqlite:///Main/Users.db")

            self.connection = self.engine.connect()
            self.session = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
        except Exception as e:
            print("Ошибка при подключении к БД\n", e)

    async def initialize_connection(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("connection initializated")

    async def is_user_exists(self, login: str, hash: str) -> bool:
        async with self.session() as session:
            stmt = select(User.id).where(and_(User.login == login, User.hash_password == hash))
            result = (await session.execute(stmt)).all()
            return bool(len(result))
        
    async def is_grade_exists(self, login_id: int, subject_id: int, grade: int, date: str) -> bool:
        async with self.session() as session:
            stmt = select(Grade.user_id).where((Grade.user_id==login_id) & (Grade.subject_id == subject_id) & (Grade.grade == grade) & (Grade.date == date))
            result = (await session.execute(stmt)).all()
            return bool(len(result))
        
    async def is_new_grade(self, login_id: int, subject_id: int, new_grade: int, date: str) -> bool:
        async with self.session() as session:
            stmt = select(Grade.grade).where((Grade.user_id == login_id) & (Grade.subject_id == subject_id) & (Grade.date == date))
            result = (await session.execute(stmt)).scalar()
            print(result)
            return True if new_grade != result else False
        
    async def is_teacher(self, login: str) -> bool:
        async with self.session() as session:
            stmt = select(User.id).where(and_(User.login == login, User.is_teacher == 1))
            result = (await session.execute(stmt)).all()
            return bool(len(result))
        
    async def add_grade(self, userid, subjectid, grade, date):
        async with self.session() as session:
            new_grade = Grade(
                user_id=userid,
                subject_id=subjectid,
                grade=grade,
                date=date
            )
            print(12)
            session.add(new_grade)
            print(13)
            await session.commit()

    async def update_grade(self, userid, subjectid, new_grade, date):
        async with self.session() as session:
            stmt = update(Grade).where((Grade.user_id == userid) & (Grade.subject_id == subjectid) & (Grade.date == date)).values(grade=new_grade)
            await session.execute(stmt)
            await session.commit()

    async def get_id_by_login(self, login: str) -> int:
        async with self.session() as session:
            stmt = select(User.id).where(User.login == login)
            result = await session.execute(stmt)
            return result.scalar()
        
    async def get_id_by_subject(self, subject: str) -> int:
        async with self.session() as session:
            stmt = select(Sudject.id).where(Sudject.name == subject)
            result = await session.execute(stmt)
            return result.scalar()

    async def get_login_by_id(self, id: int) -> str:
        async with self.session() as session:
            stmt = select(User.login).where(User.id == id)
            result = await session.execute(stmt)
            return result.scalar()
        
    async def get_subject_by_id(self, id: int) -> str:
        async with self.session() as session:
            stmt = select(Sudject.name).where(Sudject.id == id)
            result = (await session.execute(stmt)).scalar()
            return result
        
    async def get_students_login(self):
        async with self.session() as session:
            stmt = select(User.id).where(User.is_teacher == 0)
            result = (await session.execute(stmt)).scalars()
            result = [await self.get_login_by_id(id) for id in result]
            return result

    async def get_count_students(self):
        async with self.session() as session:
            stmt = select(func.count(User.id)).where(User.is_teacher == 0)
            result = await session.execute(stmt)
            return result.scalar()
        
    async def get_count_subjects(self):
        async with self.session() as session:
            stmt = select(func.count(Sudject.id))
            result = await session.execute(stmt)
            return result.scalar()
        
    async def get_grade_of_student(self, login: str) -> dict[str, list[tuple[str, int]]]:
        async with self.session() as session:
            user_id = await self.get_id_by_login(login)
            stmt = select(Grade.grade).where(Grade.user_id==user_id)
            grades = list((await session.execute(stmt)).scalars())
            stmt = select(Grade.subject_id).where(Grade.user_id==user_id)
            subs = [await self.get_subject_by_id(name) for name in list((await session.execute(stmt)).scalars())]
            stmt = select(Grade.date).where(Grade.user_id==user_id)
            dates = list((await session.execute(stmt)).scalars())

            result = {}
            for subject, grade, date in zip(subs, grades, dates):
                if subject not in result:
                    result[subject] = []
                result[subject].append((date, grade))

            return result
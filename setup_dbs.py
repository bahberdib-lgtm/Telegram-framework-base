import os

base_dir = r"c:\Users\silentcore\Downloads\Новая папка (4)"
sqlite_dir = os.path.join(base_dir, "templates/core_bases/sqlite_bot")
pg_dir = os.path.join(base_dir, "templates/core_bases/postgres_bot")

os.makedirs(sqlite_dir, exist_ok=True)
os.makedirs(pg_dir, exist_ok=True)

# SQLite Bot Base
files_sqlite = {
    "main.py": """import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config
from handlers import basic_handlers
from database.db import init_db

logging.basicConfig(level=logging.INFO)

async def main():
    await init_db()
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(basic_handlers.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
""",
    "config.py": """import os
from dataclasses import dataclass

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "YOUR_TOKEN_HERE")
    DB_NAME: str = "database.db"

config = Config()
""",
    "database": "",
    "database/__init__.py": "",
    "database/db.py": """import aiosqlite
from config import config

async def init_db():
    async with aiosqlite.connect(config.DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                telegram_id INTEGER UNIQUE,
                username TEXT,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def add_user(telegram_id: int, username: str):
    async with aiosqlite.connect(config.DB_NAME) as db:
        await db.execute('INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)', (telegram_id, username))
        await db.commit()
""",
    "handlers": "",
    "handlers/__init__.py": "",
    "handlers/basic_handlers.py": """from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from database.db import add_user

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await add_user(message.from_user.id, message.from_user.username)
    await message.answer("Hello! You have been registered in the SQLite database.")
""",
    "requirements.txt": "aiogram>=3.4.0\naiosqlite>=0.20.0\n"
}

for fname, content in files_sqlite.items():
    fpath = os.path.join(sqlite_dir, fname)
    if content == "":
        os.makedirs(fpath, exist_ok=True)
    else:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

# PostgreSQL Bot Base (SQLAlchemy async)
files_pg = {
    "main.py": """import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config
from handlers import basic_handlers
from database.db import init_db

logging.basicConfig(level=logging.INFO)

async def main():
    await init_db()
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(basic_handlers.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
""",
    "config.py": """import os
from dataclasses import dataclass

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "YOUR_TOKEN_HERE")
    DB_URL: str = os.getenv("DB_URL", "postgresql+asyncpg://user:password@localhost/dbname")

config = Config()
""",
    "database": "",
    "database/__init__.py": "",
    "database/models.py": """from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, DateTime
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String, nullable=True)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
""",
    "database/db.py": """from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import config
from database.models import Base, User

engine = create_async_engine(config.DB_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        # For production use alembic instead of create_all
        await conn.run_sync(Base.metadata.create_all)

async def add_user(telegram_id: int, username: str):
    async with AsyncSessionLocal() as session:
        user = await session.execute(
            User.__table__.select().where(User.telegram_id == telegram_id)
        )
        if not user.scalar_one_or_none():
            new_user = User(telegram_id=telegram_id, username=username)
            session.add(new_user)
            await session.commit()
""",
    "handlers": "",
    "handlers/__init__.py": "",
    "handlers/basic_handlers.py": """from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from database.db import add_user

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await add_user(message.from_user.id, message.from_user.username)
    await message.answer("Hello! You have been registered in PostgreSQL.")
""",
    "requirements.txt": "aiogram>=3.4.0\nsqlalchemy>=2.0.0\nasyncpg>=0.29.0\n"
}

for fname, content in files_pg.items():
    fpath = os.path.join(pg_dir, fname)
    if content == "":
        os.makedirs(fpath, exist_ok=True)
    else:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

print("DB setups completed.")

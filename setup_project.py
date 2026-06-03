import os
import json

base_dir = r"c:\Users\silentcore\Downloads\Новая папка (4)"

directories = [
    "generator",
    "templates/core_bases/basic_bot",
    "templates/core_bases/sqlite_bot",
    "templates/core_bases/postgres_bot",
]

for d in directories:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

# 1. Generator Script
generator_script = """import os
import shutil
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="Telegram Bot Generator")
    parser.add_argument("name", help="Name of the bot project")
    parser.add_argument("--base", default="basic_bot", help="Base template to use (e.g., basic_bot, sqlite_bot)")
    args = parser.parse_args()

    # Find template
    # This is a simplified search for the template
    templates_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    template_path = None
    for root, dirs, files in os.walk(templates_dir):
        if args.base in dirs:
            template_path = os.path.join(root, args.base)
            break
            
    if not template_path:
        print(f"Error: Template '{args.base}' not found.")
        sys.exit(1)

    project_dir = os.path.join(os.getcwd(), args.name)
    if os.path.exists(project_dir):
        print(f"Error: Directory '{args.name}' already exists.")
        sys.exit(1)

    shutil.copytree(template_path, project_dir)
    print(f"Success! Bot project '{args.name}' created based on '{args.base}'.")
    print(f"cd {args.name}")

if __name__ == "__main__":
    main()
"""
with open(os.path.join(base_dir, "generator", "bot_generator.py"), "w", encoding="utf-8") as f:
    f.write(generator_script)

# 2. Basic Bot Base
basic_bot_dir = os.path.join(base_dir, "templates/core_bases/basic_bot")
files_basic = {
    "main.py": """import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config
from handlers import basic_handlers

logging.basicConfig(level=logging.INFO)

async def main():
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

config = Config()
""",
    "handlers": "", # directory
    "handlers/__init__.py": "",
    "handlers/basic_handlers.py": """from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello! I am a basic bot.")

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Help menu: /start - start bot")
""",
    "requirements.txt": "aiogram>=3.4.0\n"
}

for fname, content in files_basic.items():
    fpath = os.path.join(basic_bot_dir, fname)
    if content == "":
        os.makedirs(fpath, exist_ok=True)
    else:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)

print("Project setup completed.")

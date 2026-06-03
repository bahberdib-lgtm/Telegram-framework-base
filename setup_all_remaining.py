import os

base_dir = r"c:\Users\silentcore\Downloads\Новая папка (4)"
templates_dir = os.path.join(base_dir, "templates")

categories = {
    "admin_bases": ["admin_bot", "moderation_bot", "security_bot"],
    "community_bases": ["welcome_bot", "verification_bot", "ticket_support_bot"],
    "economy_bases": ["economy_bot", "giveaway_bot", "referral_bot"],
    "business_bases": ["shop_bot", "subscription_bot", "crm_bot"],
    "ai_bases": ["ai_assistant_bot", "ai_image_bot", "ai_translator_bot"],
    "entertainment_bases": ["music_bot", "quiz_bot", "rpg_bot"],
    "utility_bases": ["file_storage_bot", "notes_bot", "url_shortener_bot"],
    "developer_bases": ["plugin_system_bot", "api_client_bot", "webhook_bot"],
}

basic_main_py = """import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    # TODO: Add handlers here
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
"""

basic_config_py = """import os
from dataclasses import dataclass

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "YOUR_TOKEN_HERE")

config = Config()
"""

for category, bases in categories.items():
    cat_dir = os.path.join(templates_dir, category)
    os.makedirs(cat_dir, exist_ok=True)
    
    for base in bases:
        base_path = os.path.join(cat_dir, base)
        os.makedirs(base_path, exist_ok=True)
        
        # Create standard files
        with open(os.path.join(base_path, "main.py"), "w", encoding="utf-8") as f:
            f.write(basic_main_py)
            
        with open(os.path.join(base_path, "config.py"), "w", encoding="utf-8") as f:
            f.write(basic_config_py)
            
        with open(os.path.join(base_path, "requirements.txt"), "w", encoding="utf-8") as f:
            f.write("aiogram>=3.4.0\n")
            
        with open(os.path.join(base_path, "README.md"), "w", encoding="utf-8") as f:
            f.write(f"# {base.replace('_', ' ').title()}\n\n")
            f.write("This is a template for the Telegram Bot Generator.\n")
            f.write("Specific logic for this bot type should be implemented here.\n")

print("All remaining bases setup completed.")

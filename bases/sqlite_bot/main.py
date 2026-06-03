import sqlite3
from telegram.ext import Application, CommandHandler

TOKEN = "PUT_TOKEN_HERE"

db = sqlite3.connect("bot.db", check_same_thread=False)
db.execute('''
CREATE TABLE IF NOT EXISTS users(
user_id INTEGER PRIMARY KEY,
username TEXT
)
''')

async def start(update, context):
    user = update.effective_user
    db.execute(
        "INSERT OR IGNORE INTO users(user_id, username) VALUES (?, ?)",
        (user.id, user.username)
    )
    db.commit()
    await update.message.reply_text("SQLite Bot Base")

async def stats(update, context):
    count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    await update.message.reply_text(f"Users: {count}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stats", stats))
app.run_polling()
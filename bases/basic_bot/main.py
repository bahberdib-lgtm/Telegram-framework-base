from telegram.ext import Application, CommandHandler

TOKEN = "PUT_TOKEN_HERE"

async def start(update, context):
    await update.message.reply_text("Basic Bot Base")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
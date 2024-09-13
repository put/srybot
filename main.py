from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

async def addword(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open("words.txt", "a+", encoding="utf-8") as f:
        f.seek(0)
        words = f.read().splitlines()
        if len(context.args) < 1:
            await update.message.reply_text("Should probably mention a word silly")
            return
        apology = " ".join(context.args).strip().lower()
        for word in words:
            if word.lower() == apology:
                await update.message.reply_text(f"{word.lower()} is already in the word list ))")
                return
        f.write(f"{apology}\n")
        await update.message.reply_text(f"{apology} was added to the word list ))")



async def find_apologies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open("words.txt", "r", encoding="utf-8") as f:
        words = f.read().splitlines()
        for word in words:
            if word in update.message.text.lower():
                await update.message.reply_text("Is that an apology?!")
                return

def get_token_str(filename: str) -> str:
    txt = ""
    with open(filename, 'r') as f:
        txt = f.read()
    return txt

def main() -> None:
    application = Application.builder().token(get_token_str(".token")).build()
    application.add_handler(CommandHandler("addword", addword))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_apologies))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
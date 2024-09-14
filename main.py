from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from typing import List, Self
import json

class TGUser:
    def __init__(self, id: int, apology_count: int) -> Self:
        self.id = id
        self.apology_count = apology_count

class TGUserCollection:
    def __init__(self, users: List[TGUser]):
        self.users = users

    @staticmethod
    def get_users(path: str) -> Self:
        test: TGUserCollection = TGUserCollection([])
        with open(path, "a+") as f:
            f.seek(0)
            read_txt = f.read()
            if len(read_txt) > 0:
                test = TGUserCollection(**json.loads(read_txt))
                test.users = [TGUser(**user) for user in test.users]
        return test
    
    @staticmethod
    def make_user(path: str, id: int) -> TGUser:
        users: TGUserCollection = TGUserCollection.get_users(path)
        user = next((u for u in users.users if u.id == id), None)
        if not user:
            user = TGUser(id, 0)
            users.users.append(user)
            with open(path, "w") as f:
                f.write(json.dumps(users, default=lambda o: o.__dict__))
            return user
        else:
            return user
        
    @staticmethod
    def update(path: str, id: int) -> None:
        users: TGUserCollection = TGUserCollection.get_users(path)
        index = next((i for i, user in enumerate(users.users) if user.id == id), None)
        if index is not None:
            users.users[index].apology_count = users.users[index].apology_count + 1
            with open(path, "w") as f:
                f.write(json.dumps(users, default=lambda o: o.__dict__))


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
                users: TGUserCollection = TGUserCollection.get_users("users.json")
                user = next((u for u in users.users if u.id == update.effective_user.id), None)
                if not user:
                    user = TGUserCollection.make_user("users.json", update.effective_user.id)
                user.apology_count = user.apology_count + 1
                await update.message.reply_text(f"No need to apologize! You've done this {user.apology_count} time{'' if user.apology_count == 1 else 's'} now.")
                TGUserCollection.update("users.json", user.id)
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
from fastapi import FastAPI
import uvicorn

from dotenv import load_dotenv
from app.TgBot.bot import TelegramBot
import os
import asyncio

load_dotenv()

app = FastAPI()


if __name__ == "__main__":
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    YOUR_USER_ID = os.getenv("YOUR_USER_ID")

    bot = TelegramBot(TOKEN, int(YOUR_USER_ID))
    
    # Запуск бота в асинхронном режиме
    loop = asyncio.get_event_loop()
    loop.create_task(bot.start_polling())
    
    # Запуск FastAPI сервер
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


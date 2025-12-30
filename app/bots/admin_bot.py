from aiogram import Bot, Dispatcher
from app.config import Config

admin_bot = Bot(token=Config.ADMIN_BOT_TOKEN)
admin_dp = Dispatcher()

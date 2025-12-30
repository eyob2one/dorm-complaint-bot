from aiogram import Bot, Dispatcher
from app.config import Config

student_bot = Bot(token=Config.STUDENT_BOT_TOKEN)
student_dp = Dispatcher()

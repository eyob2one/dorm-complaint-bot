import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    STUDENT_BOT_TOKEN = os.getenv("STUDENT_BOT_TOKEN")
    ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
    DATABASE_URL = os.getenv("DATABASE_URL")
    ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

category_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔒 Locker / Furniture")],
        [KeyboardButton(text="🔊 Noise / Disturbance")],
        [KeyboardButton(text="💡 Electricity")],
        [KeyboardButton(text="🚿 Water / Plumbing")],
        [KeyboardButton(text="🧹 Cleanliness")],
        [KeyboardButton(text="🛡 Security")],
        [KeyboardButton(text="🛏 Roommate Issues")],
        [KeyboardButton(text="❓ Other")],
    ],
    resize_keyboard=True
)

anonymous_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Send with my name")],
        [KeyboardButton(text="Send anonymously")],
    ],
    resize_keyboard=True
)

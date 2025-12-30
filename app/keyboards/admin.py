from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def complaint_actions_keyboard(complaint_id: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🟡 In Progress",
                    callback_data=f"in_progress:{complaint_id}"
                ),
                InlineKeyboardButton(
                    text="✅ Resolved",
                    callback_data=f"resolved:{complaint_id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❌ Rejected",
                    callback_data=f"rejected:{complaint_id}"
                )
            ]
        ]
    )

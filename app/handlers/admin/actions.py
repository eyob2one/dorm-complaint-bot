from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.config import Config
from app.db.database import get_db
from app.db.crud import update_complaint_status
from app.bots.student_bot import student_bot

router = Router()

STATUS_MAP = {
    "in_progress": "🟡 In Progress",
    "resolved": "✅ Resolved",
    "rejected": "❌ Rejected",
}

def is_admin(user_id: int) -> bool:
    return user_id == Config.ADMIN_CHAT_ID


@router.callback_query(F.data.contains(":"))
async def handle_action(callback: CallbackQuery):
    # 🔒 Admin check FIRST
    if not is_admin(callback.from_user.id):
        await callback.answer("Unauthorized", show_alert=True)
        return

    action, complaint_id = callback.data.split(":")

    async for db in get_db():
        complaint = await update_complaint_status(db, complaint_id, action)

    # 📢 Notify student (only if not anonymous)
    if not complaint.is_anonymous and complaint.student_telegram_id:
        await student_bot.send_message(
            complaint.student_telegram_id,
            (
                f"📢 Your dorm complaint has been updated.\n\n"
                f"Category: {complaint.category}\n"
                f"Status: {STATUS_MAP[action]}"
            )
        )

    # ✏️ Update admin message
    if callback.message.caption:
        await callback.message.edit_caption(
            callback.message.caption + f"\n\nStatus Updated: {STATUS_MAP[action]}"
        )
    else:
        await callback.message.edit_text(
            callback.message.text + f"\n\nStatus Updated: {STATUS_MAP[action]}"
        )

    await callback.answer("Status updated successfully")

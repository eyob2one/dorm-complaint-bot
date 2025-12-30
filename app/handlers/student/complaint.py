from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from app.keyboards.student import category_keyboard, anonymous_keyboard
from app.db.crud import create_complaint
from app.db.database import get_db
from app.bots.admin_bot import admin_bot
from app.config import Config

router = Router()

class ComplaintState(StatesGroup):
    category = State()
    description = State()
    image = State()
    anonymous = State()

@router.message(F.text == "/complaint")
async def start_complaint(message: Message, state: FSMContext):
    await message.answer("Select complaint category:", reply_markup=category_keyboard)
    await state.set_state(ComplaintState.category)

@router.message(ComplaintState.category)
async def get_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("Describe the issue:")
    await state.set_state(ComplaintState.description)

@router.message(ComplaintState.description)
async def get_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Send an image (or type /skip):")
    await state.set_state(ComplaintState.image)

@router.message(ComplaintState.image, F.photo)
async def get_image(message: Message, state: FSMContext):
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Send anonymously?", reply_markup=anonymous_keyboard)
    await state.set_state(ComplaintState.anonymous)

@router.message(ComplaintState.image)
async def skip_image(message: Message, state: FSMContext):
    await state.update_data(image=None)
    await message.answer("Send anonymously?", reply_markup=anonymous_keyboard)
    await state.set_state(ComplaintState.anonymous)

@router.message(ComplaintState.anonymous)
async def finalize(message: Message, state: FSMContext):
    data = await state.get_data()
    is_anonymous = message.text == "Send anonymously"

    async for db in get_db():
        complaint = await create_complaint(
            db=db,
            student_telegram_id=str(message.from_user.id),
            category=data["category"],
            description=data["description"],
            image_file_id=data["image"],
            is_anonymous=is_anonymous,
        )

    text = (
        f"📢 New Dorm Complaint\n\n"
        f"Category: {complaint.category}\n"
        f"Description: {complaint.description}\n"
        f"Student: {'Anonymous' if is_anonymous else complaint.student_telegram_id}\n"
        f"Status: Pending"
    )

    keyboard = complaint_actions_keyboard(str(complaint.id))

    if complaint.image_file_id:
        await admin_bot.send_photo(
            Config.ADMIN_CHAT_ID,
            complaint.image_file_id,
            caption=text,
            reply_markup=keyboard
        )
    else:
        await admin_bot.send_message(
            Config.ADMIN_CHAT_ID,
            text,
            reply_markup=keyboard
        )

    await message.answer("✅ Complaint submitted successfully.")
    await state.clear()

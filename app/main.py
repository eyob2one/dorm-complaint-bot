import asyncio
from app.bots.student_bot import student_dp, student_bot
from app.bots.admin_bot import admin_dp, admin_bot
from app.handlers.student.complaint import router as student_router
from app.handlers.admin.actions import router as admin_router

admin_dp.include_router(admin_router)
student_dp.include_router(student_router)

async def main():
    await asyncio.gather(
        student_dp.start_polling(student_bot),
        admin_dp.start_polling(admin_bot),
    )

if __name__ == "__main__":
    asyncio.run(main())

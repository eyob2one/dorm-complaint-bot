from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Complaint
from sqlalchemy import select
from datetime import datetime

async def create_complaint(
    db: AsyncSession,
    student_telegram_id: str,
    category: str,
    description: str,
    image_file_id: str | None,
    is_anonymous: bool
):
    complaint = Complaint(
        student_telegram_id=None if is_anonymous else student_telegram_id,
        category=category,
        description=description,
        image_file_id=image_file_id,
        is_anonymous=is_anonymous,
    )
    db.add(complaint)
    await db.commit()
    await db.refresh(complaint)
    return complaint

async def update_status(db: AsyncSession, complaint_id, status: str):
    result = await db.execute(
        select(Complaint).where(Complaint.id == complaint_id)
    )
    complaint = result.scalar_one()
    complaint.status = status
    complaint.updated_at = datetime.utcnow()
    await db.commit()

async def get_complaint(db, complaint_id):
    result = await db.execute(
        select(Complaint).where(Complaint.id == complaint_id)
    )
    return result.scalar_one()

async def update_complaint_status(db, complaint_id, status: str):
    complaint = await get_complaint(db, complaint_id)
    complaint.status = status
    complaint.updated_at = datetime.utcnow()
    await db.commit()
    return complaint
from aiogram import Router, types
from aiogram.filters import Command

from config import ADMIN_ID
from keyboards.buttons import admin_keyboard


router = Router()


@router.message(Command("panel"))
async def panel(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "⚙️ پنل مدیریت",
        reply_markup=admin_keyboard()
    )

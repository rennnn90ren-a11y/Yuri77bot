from aiogram import Router, types
from aiogram.filters import CommandStart

from config import ADMIN_ID
from keyboards.buttons import admin_keyboard


router = Router()



@router.message(CommandStart())
async def admin_start(
    message: types.Message
):

    if message.from_user.id == ADMIN_ID:

        await message.answer(
            "پنل مدیریت:",
            reply_markup=admin_keyboard()
        )

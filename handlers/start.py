from aiogram import Router, types
from aiogram.filters import CommandStart

from database import (
    find_file,
    get_channels
)

from keyboards.buttons import join_keyboard


router = Router()


user_chapters = {}


async def is_member(bot, user_id):

    channels = get_channels()

    for channel in channels:

        try:

            member = await bot.get_chat_member(
                channel,
                user_id
            )

            if member.status in [
                "left",
                "kicked"
            ]:
                return False

        except:

            return False

    return True



@router.message(CommandStart())
async def start_handler(
    message: types.Message
):

    args = message.text.split()


    if len(args) > 1:

        code = args[1]

        user_chapters[
            message.from_user.id
        ] = code


    if not await is_member(
        message.bot,
        message.from_user.id
    ):

        await message.answer(
            "برای دریافت چپتر ابتدا عضو کانال‌ها شوید:",
            reply_markup=join_keyboard(
                get_channels()
            )
        )

        return


    code = user_chapters.get(
        message.from_user.id
    )


    if code:

        file_id = find_file(code)

        if file_id:

            await message.answer_document(
                file_id,
                caption=f"📖 Chapter {code}"
            )

        else:

            await message.answer(
                "❌ چپتر پیدا نشد."
            )



@router.callback_query(
    lambda c: c.data == "check_join"
)
async def check_join(
    callback: types.CallbackQuery
):

    if await is_member(
        callback.bot,
        callback.from_user.id
    ):

        code = user_chapters.get(
            callback.from_user.id
        )


        if code:

            file_id = find_file(code)


            if file_id:

                await callback.message.answer_document(
                    file_id,
                    caption=f"📖 Chapter {code}"
                )

            else:

                await callback.message.answer(
                    "❌ فایل موجود نیست."
                )

        else:

            await callback.message.answer(
                "لینک چپتر را دوباره باز کن."
            )


    else:

        await callback.answer(
            "هنوز عضو کانال‌ها نشدی!",
            show_alert=True
        )

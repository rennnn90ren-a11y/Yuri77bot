from aiogram import Router, types

from config import ADMIN_ID

from database import (
    add_channel,
    delete_channel,
    get_channels
)


router = Router()


channel_mode = {}



@router.callback_query(
    lambda c: c.data == "add_channel"
)
async def add_channel_start(
    call: types.CallbackQuery
):

    if call.from_user.id != ADMIN_ID:
        return


    channel_mode[
        call.from_user.id
    ] = "add"


    await call.message.answer(
        "آیدی کانال را ارسال کن:\n"
        "مثال:\n@mychannel"
    )



@router.callback_query(
    lambda c: c.data == "remove_channel"
)
async def remove_channel_start(
    call: types.CallbackQuery
):

    if call.from_user.id != ADMIN_ID:
        return


    channels = get_channels()


    if not channels:

        await call.message.answer(
            "هیچ کانالی ثبت نشده."
        )

        return



    text = "کانال‌های ثبت شده:\n\n"


    for ch in channels:

        text += f"{ch}\n"


    text += (
        "\nآیدی کانالی که می‌خواهی حذف شود را بفرست."
    )


    channel_mode[
        call.from_user.id
    ] = "remove"


    await call.message.answer(
        text
    )



@router.message(
    lambda m:
    m.from_user.id == ADMIN_ID
)
async def channel_action(
    message: types.Message
):

    mode = channel_mode.get(
        message.from_user.id
    )


    if not mode:
        return


    channel = message.text.strip()


    if mode == "add":

        add_channel(
            channel
        )

        await message.answer(
            "✅ کانال اضافه شد"
        )


    elif mode == "remove":

        delete_channel(
            channel
        )

        await message.answer(
            "🗑 کانال حذف شد"
        )


    del channel_mode[
        message.from_user.id
]

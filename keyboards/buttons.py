from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def admin_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="📄 افزودن چپتر",
                    callback_data="add_file"
                )
            ],

            [
                InlineKeyboardButton(
                    text="➕ افزودن کانال",
                    callback_data="add_channel"
                )
            ],

            [
                InlineKeyboardButton(
                    text="➖ حذف کانال",
                    callback_data="remove_channel"
                )
            ],

        ]
    )



def join_keyboard(channels):

    buttons = []


    for channel in channels:

        buttons.append(
            [
                InlineKeyboardButton(
                    text="عضویت در کانال",
                    url=f"https://t.me/{channel.replace('@','')}"
                )
            ]
        )


    buttons.append(
        [
            InlineKeyboardButton(
                text="✅ بررسی عضویت",
                callback_data="check_join"
            )
        ]
    )


    return InlineKeyboardMarkup(
        inline_keyboard=buttons
                )

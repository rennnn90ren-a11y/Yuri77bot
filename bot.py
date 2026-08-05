import os
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F

# توکن را در محیط قرار بده
TOKEN = os.getenv("8447879722:AAEJwwzqM58bobKqiZqQ6U-dqv3JmvCNZbI")

# آیدی عددی ادمین خودت را اینجا بگذار
ADMIN_ID = 8255361263

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

db = sqlite3.connect("bot.db")
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS files(
    code TEXT PRIMARY KEY,
    file_id TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS channels(
    username TEXT PRIMARY KEY
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS settings(
    name TEXT PRIMARY KEY,
    value TEXT
)
""")

db.commit()


def admin(user_id):
    return user_id == ADMIN_ID


async def check_member(user_id):
    cur.execute("SELECT username FROM channels")
    channels = cur.fetchall()

    for ch in channels:
        try:
            member = await bot.get_chat_member(
                ch[0],
                user_id
            )

            if member.status in ["left", "kicked"]:
                return False
        except:
            return False

    return True


def join_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[])

    cur.execute("SELECT username FROM channels")
    for ch in cur.fetchall():
        kb.inline_keyboard.append([
            InlineKeyboardButton(
                text="عضویت در کانال",
                url=f"https://t.me/{ch[0].replace('@','')}"
            )
        ])

    kb.inline_keyboard.append([
        InlineKeyboardButton(
            text="بررسی عضویت ✅",
            callback_data="check"
        )
    ])

    return kb


@dp.message(CommandStart())
async def start(message: types.Message):

    args = message.text.split()

    if len(args) == 1:
        await message.answer(
            "سلام 👋\nربات دریافت چپتر آماده است."
        )
        return

    code = args[1]

    if not await check_member(message.from_user.id):
        await message.answer(
            "برای دریافت فایل ابتدا عضو کانال‌ها شوید:",
            reply_markup=join_keyboard()
        )
        return

    cur.execute(
        "SELECT file_id FROM files WHERE code=?",
        (code,)
    )

    result = cur.fetchone()

    if result:
        await message.answer_document(
            result[0],
            caption=f"Chapter {code}"
        )
    else:
        await message.answer(
            "این چپتر پیدا نشد."
)
      @dp.callback_query(F.data == "check")
async def check_button(callback: types.CallbackQuery):

    if await check_member(callback.from_user.id):
        await callback.message.answer(
            "✅ عضویت تایید شد.\nحالا دوباره روی لینک چپتر بزن."
        )
    else:
        await callback.answer(
            "هنوز عضو همه کانال‌ها نشدی!",
            show_alert=True
        )


@dp.message(Command("panel"))
async def panel(message: types.Message):

    if not admin(message.from_user.id):
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ افزودن کانال",
                    callback_data="add_channel"
                )
            ],
            [
                InlineKeyboardButton(
                    text="➖ حذف کانال",
                    callback_data="del_channel"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📄 افزودن چپتر",
                    callback_data="add_file"
                )
            ]
        ]
    )

    await message.answer(
        "پنل مدیریت:",
        reply_markup=kb
    )


@dp.callback_query(F.data == "add_channel")
async def add_channel(callback: types.CallbackQuery):

    if not admin(callback.from_user.id):
        return

    await callback.message.answer(
        "آیدی کانال را بفرست:\nمثال:\n@mychannel"
    )


@dp.message(F.text.startswith("@"))
async def save_channel(message: types.Message):

    if not admin(message.from_user.id):
        return

    channel = message.text.strip()

    cur.execute(
        "INSERT OR IGNORE INTO channels VALUES(?)",
        (channel,)
    )

    db.commit()

    await message.answer(
        "✅ کانال اضافه شد"
    )


@dp.callback_query(F.data == "del_channel")
async def delete_channel(callback: types.CallbackQuery):

    if not admin(callback.from_user.id):
        return

    cur.execute("SELECT username FROM channels")

    channels = cur.fetchall()

    kb = InlineKeyboardMarkup(
        inline_keyboard=[]
    )

    for ch in channels:
        kb.inline_keyboard.append([
            InlineKeyboardButton(
                text=ch[0],
                callback_data=f"remove_{ch[0]}"
            )
        ])

    await callback.message.answer(
        "کانال برای حذف:",
        reply_markup=kb
    )


@dp.callback_query(F.data.startswith("remove_"))
async def remove_channel(callback: types.CallbackQuery):

    if not admin(callback.from_user.id):
        return

    ch = callback.data.replace(
        "remove_",
        ""
    )

    cur.execute(
        "DELETE FROM channels WHERE username=?",
        (ch,)
    )

    db.commit()

    await callback.message.answer(
        "🗑 کانال حذف شد"
)
@dp.callback_query(F.data == "add_file")
async def add_file_start(callback: types.CallbackQuery):

    if not admin(callback.from_user.id):
        return

    await callback.message.answer(
        "کد چپتر را بفرست:\nمثال:\n1_2"
    )

    # ذخیره حالت موقت ادمین
    await callback.message.answer(
        "بعد از ارسال کد، فایل PDF را ارسال کن."
    )


# نگهداری موقت کد چپتر
waiting_files = {}


@dp.message(F.text)
async def get_file_code(message: types.Message):

    if not admin(message.from_user.id):
        return

    text = message.text.strip()

    if "_" in text or text.isdigit():

        waiting_files[message.from_user.id] = text

        await message.answer(
            "حالا فایل PDF را ارسال کن 📄"
        )


@dp.message(F.document)
async def save_pdf(message: types.Message):

    if not admin(message.from_user.id):
        return

    user_id = message.from_user.id

    if user_id not in waiting_files:
        return

    code = waiting_files[user_id]

    file_id = message.document.file_id

    cur.execute(
        """
        INSERT OR REPLACE INTO files(code,file_id)
        VALUES(?,?)
        """,
        (code, file_id)
    )

    db.commit()

    del waiting_files[user_id]

    await message.answer(
        f"✅ چپتر {code} ذخیره شد"
    )


@dp.message(Command("stats"))
async def stats(message: types.Message):

    if not admin(message.from_user.id):
        return

    cur.execute(
        "SELECT COUNT(*) FROM files"
    )

    files = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM channels"
    )

    channels = cur.fetchone()[0]

    await message.answer(
        f"""
📊 آمار ربات

📄 تعداد چپترها: {files}
📢 کانال‌ها: {channels}
"""
    )


async def main():

    print("Bot Started")

    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

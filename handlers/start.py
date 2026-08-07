from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from config import ADMIN_ID

router = Router()  # حتماً این خط باشه!

# دیکشنری برای ذخیره چپترهای کاربر
user_chapters = {}

# تابع چک کردن عضو بودن (باید کامل شه)
async def is_member(bot, user_id):
    # اینجا کد چک کردن عضویت
    return True  # موقتی

# تابع دریافت کانال‌ها
def get_channels():
    return ["@channel1", "@channel2"]  # موقتی

# تابع دکمه‌های جوین
def join_keyboard(channels):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    buttons = []
    for ch in channels:
        buttons.append([InlineKeyboardButton(text=f"عضویت در {ch}", url=f"https://t.me/{ch[1:]}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# تابع پیدا کردن فایل
def find_file(code):
    # اینجا کد پیدا کردن فایل
    return None  # موقتی

@router.message(CommandStart())
async def start_handler(message: types.Message):
    args = message.text.split()
    
    # استارت معمولی
    if len(args) == 1:
        await message.answer("سلام 👋 به ربات خوش اومدی!")
        return
    
    # استارت از لینک چپتر
    code = args[1]
    user_chapters[message.from_user.id] = code
    
    if not await is_member(message.bot, message.from_user.id):
        await message.answer(
            "برای دریافت چپتر ابتدا عضو کانال‌ها شوید:",
            reply_markup=join_keyboard(get_channels())
        )
        return
    
    file_id = find_file(code)
    if file_id:
        await message.answer_document(file_id, caption=f"📖 Chapter {code}")
    else:
        await message.answer("❌ فایل پیدا نشد!")

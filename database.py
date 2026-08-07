from aiogram import Router, types
from aiogram.filters import CommandStart
from config import ADMIN_ID
from database import find_file  # ← این رو درست کن!

router = Router()

# دیکشنری برای ذخیره کد چپتر کاربر
user_chapters = {}

# لیست کانال‌های اجباری (از دیتابیس میخونه)
from database import get_channels as db_get_channels

async def is_member(bot, user_id):
    channels = db_get_channels()
    if not channels:  # اگر کانالی تنظیم نشده، اجازه بده
        return True
    
    for channel in channels:
        try:
            member = await bot.get_chat_member(f"@{channel}", user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

def join_keyboard(channels):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    buttons = []
    for ch in channels:
        clean_ch = ch.replace("@", "")
        buttons.append([InlineKeyboardButton(
            text=f"📢 عضویت در @{clean_ch}", 
            url=f"https://t.me/{clean_ch}"
        )])
    buttons.append([InlineKeyboardButton(
        text="✅ بررسی عضویت", 
        callback_data="check_membership"
    )])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(CommandStart())
async def start_handler(message: types.Message):
    args = message.text.split()
    
    # استارت معمولی
    if len(args) == 1:
        await message.answer(
            "👋 سلام! به ربات خوش اومدی!\n"
            "برای دریافت چپتر از لینک مخصوص استفاده کن."
        )
        return
    
    # استارت از لینک چپتر
    code = args[1]
    user_chapters[message.from_user.id] = code
    
    # چک کردن عضویت
    if not await is_member(message.bot, message.from_user.id):
        channels = db_get_channels()
        await message.answer(
            "🔒 برای دریافت چپتر ابتدا عضو کانال‌های زیر شوید:",
            reply_markup=join_keyboard(channels)
        )
        return
    
    # پیدا کردن فایل از دیتابیس
    file_id = find_file(code)
    if file_id:
        await message.answer_document(
            file_id,
            caption=f"📖 چپتر {code}"
        )
    else:
        await message.answer(f"❌ چپتر {code} پیدا نشد!")

# هندلر برای دکمه بررسی عضویت
@router.callback_query(lambda c: c.data == "check_membership")
async def check_membership(call: types.CallbackQuery):
    code = user_chapters.get(call.from_user.id)
    if not code:
        await call.message.edit_text("❌ لینک نامعتبر! دوباره تلاش کن.")
        return
    
    if not await is_member(call.bot, call.from_user.id):
        await call.answer("❌ هنوز عضو همه کانال‌ها نشدی!", show_alert=True)
        return
    
    file_id = find_file(code)
    if file_id:
        await call.message.delete()
        await call.message.answer_document(
            file_id,
            caption=f"📖 چپتر {code}"
        )
    else:
        await call.message.edit_text(f"❌ چپتر {code} پیدا نشد!")

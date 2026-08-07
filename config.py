import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN در متغیرهای محیطی تنظیم نشده!")

ADMIN_ID = 8255361263  # ← اینو با آیدی واقعى خودت عوض کن

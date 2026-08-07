import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

print("🔍 BOT_TOKEN موجود است:", "بله" if BOT_TOKEN else "خیر")
print("🔍 ADMIN_ID:", ADMIN_ID)

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN در متغیرهای محیطی تنظیم نشده!")

ADMIN_ID = 8255361263

import os


BOT_TOKEN = os.getenv("8447879722:AAEJwwzqM58bobKqiZqQ6U-dqv3JmvCNZbI")

# آیدی عددی ادمین
ADMIN_ID = 8255361263


if not BOT_TOKEN:
    raise ValueError(
        "BOT_TOKEN تنظیم نشده است!"
    )

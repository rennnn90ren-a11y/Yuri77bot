import asyncio

from aiogram import Bot, Dispatcher


from config import BOT_TOKEN

from database import setup_database


from handlers.start import router as start_router
from handlers.admin import router as admin_router
from handlers.channels import router as channels_router
from handlers.files import router as files_router



async def main():

    setup_database()


    bot = Bot(
        token=BOT_TOKEN
    )


    dp = Dispatcher()


    dp.include_router(
        start_router
    )

    dp.include_router(
        admin_router
    )

    dp.include_router(
        channels_router
    )

    dp.include_router(
        files_router
    )


    print(
        "Bot is running..."
    )


    await dp.start_polling(
        bot
    )



if __name__ == "__main__":

    asyncio.run(main())

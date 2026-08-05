@router.message(CommandStart())
async def start_handler(message: types.Message):

    args = message.text.split()

    # استارت معمولی
    if len(args) == 1:

        await message.answer(
            "سلام 👋"
        )

        return


    # استارت از لینک چپتر
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


    file_id = find_file(code)

    if file_id:

        await message.answer_document(
            file_id,
            caption=f"📖 Chapter {code}"
        )

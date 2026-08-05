from aiogram import Router, types

from config import ADMIN_ID

from database import save_file


router = Router()


file_step = {}



@router.callback_query(
    lambda c: c.data == "add_file"
)
async def add_file_start(
    call: types.CallbackQuery
):

    if call.from_user.id != ADMIN_ID:
        return


    file_step[
        call.from_user.id
    ] = "code"


    await call.message.answer(
        "کد چپتر را بفرست:\n"
        "مثال:\n1_2"
    )



@router.message(
    lambda m:
    m.from_user.id == ADMIN_ID
    and m.text is not None
)
async def receive_code(
    message: types.Message
):

    state = file_step.get(
        message.from_user.id
    )


    if state != "code":
        return


    file_step[
        message.from_user.id
    ] = message.text.strip()


    await message.answer(
        "حالا PDF را ارسال کن 📄"
    )



@router.message(
    lambda m:
    m.from_user.id == ADMIN_ID
    and m.document is not None
)
async def receive_pdf(
    message: types.Message
):

    code = file_step.get(
        message.from_user.id
    )


    if not code:
        return


    save_file(
        code,
        message.document.file_id
    )


    del file_step[
        message.from_user.id
    ]


    await message.answer(
        f"✅ چپتر {code} ذخیره شد"
  )

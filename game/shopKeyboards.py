from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# shop car select
shopMarkSeletIk = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("LADA (ВАЗ)", callback_data="shopMarkSelectedLADA")]
])

async def buyCarKeyboard(carName):
    print(carName)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("💸 Купить 💸", callback_data=f"buyCar{carName}")]
    ])

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# shop car select
shopMarkSeletIk = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("ЭКОНОМ КЛАСС 🥉", callback_data="shopMarkSelectedEconom")],
    [InlineKeyboardButton("КОМФОРТ 🥈", callback_data="shopMarkSelectedComfort")]
])

async def buyCarKeyboard(carName):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("💸 Купить 💸", callback_data=f"buyCar{carName}")]
    ])

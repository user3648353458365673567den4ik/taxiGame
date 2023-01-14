from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# register accept ik
registerConfrmIk = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("Соглашаюсь ✅", callback_data="registerConfirmIkAgree")],
    [InlineKeyboardButton("Отказываюсь ❌", callback_data="registerConfirmIkRefuse")]
])

from .shopKeyboards import shopMarkSeletIk, buyCarKeyboard
from .shopConfig import CARS


async def callShop(message, user, bot):
    await message.answer("Выберите марку автомобиля 🚙", reply_markup=shopMarkSeletIk)

async def selectCar(bot, user):
    for car in CARS["ECONOM"]:
        for name, price in car.items():
            await bot.send_message(user.id, f"<b>🚗 АВТОМОБИЛЬ {name} 🚗</b>\n<b>ЦЕНА: <i>{price}</i>₽ 💰</b>", parse_mode="HTML",
            reply_markup=await buyCarKeyboard(name))

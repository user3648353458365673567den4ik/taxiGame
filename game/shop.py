from .shopKeyboards import shopMarkSeletIk, buyCarKeyboard
from .shopConfig import CARS


async def callShop(message, user, bot):
    await message.answer("🎖 Выберите класс автомобиля 🎖", reply_markup=shopMarkSeletIk)

async def selectCar(carClass, bot, user):
    if carClass == "econom":
        for car in CARS["ECONOM"]:
            for name, params in car.items():
                price = params[0]
                max_speed = params[1]
                await bot.send_message(user.id, f"<b>🚗 АВТОМОБИЛЬ {name} 🚗</b>\n<b>ЦЕНА: <i>{price}</i>₽ 💰</b>\n<b>МАКСИМАЛЬНАЯ СКОРОСТЬ: <i>{max_speed}km/h</i></b>", parse_mode="HTML",
                reply_markup=await buyCarKeyboard(name))
    elif carClass == "comfort":
        for car in CARS["COMFORT"]:
            for name, params in car.items():
                price = params[0]
                max_speed = params[1]
                await bot.send_message(user.id, f"<b>🚗 АВТОМОБИЛЬ {name} 🚗</b>\n<b>ЦЕНА: <i>{price}</i>₽ 💰</b>\n<b>МАКСИМАЛЬНАЯ СКОРОСТЬ: <i>{max_speed}km/h</i></b>", parse_mode="HTML",
                reply_markup=await buyCarKeyboard(name))

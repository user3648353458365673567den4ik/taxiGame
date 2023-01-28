from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from keyboards import registerConfrmIk
from database import *
from game.shop import *
from aiogram.dispatcher.filters import Text
from game.shopConfig import CARS


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

dbInit()


async def userExistsCheck(message, userId):
    if not isInDb(userId):
        await message.answer("Извините, но сначала вам нужно стать игроком..")
        return False
    else:
        return True


# handlers
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    if not isInDb(message.from_user.id):
        await bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEHKh5jub0Na7Xhbtdn6IVVMh1KivqXYwACjAADFkJrCkKO_mIXPU3iLQQ")
        await message.answer("🚕 Приветствуем в симуляторе Такси!\n💰 В этой игре вы сможете зарабатывать виртуальную валюту просто за ожидание, прокачиваясь! 😃")
        await message.answer('Нажимая кнопку "Продолжить" вы соглашаетесь со следующими условиями:\n1. Вы будете внесены в базу данных бота с целью сохранения прогресса\n2. Вы обязуетесь выполнять правила игры',
            reply_markup=registerConfrmIk)
    else:
        await message.answer(f"Здравствуйте, {getUserStats(message.from_user.id)[1]}! 👋\n📜 Чтобы узнать список команд на введите /help 📜")

@dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    if not await userExistsCheck(message, message.from_user.id):
        return
    await message.answer("/stats - ваша статистика 📝\n/shop - автосалон 🚙")

@dp.message_handler(commands=['stats'])
async def command_stats(message: types.Message):
    if not await userExistsCheck(message, message.from_user.id):
        return
    data = getUserStats(message.from_user.id)
    currentCarSpd = getCurrentCarSpeed(message.from_user.id)
    await message.answer(f"⭐️ СТАТИСТИКА ИГРОКА ⭐️\n\n🔸 Ваш ID: <b>{data[0]}</b> 🗝️\n🔸 Ваш никнейм: <b>{data[1]}</b> 📕\n🔸 Ваш баланс: <b>{data[2]}₽ 💰</b>\n🔸 Ваша машина: <b>{data[3]} ({currentCarSpd} km/h) 🚖</b>", parse_mode="HTML")

@dp.message_handler(commands=['shop'])
async def command_shop(message: types.Message):
    if not await userExistsCheck(message, message.from_user.id):
        return
    await callShop(message, message.from_user, bot)


# callbacks
@dp.callback_query_handler(Text(startswith="registerConfirmIk"))
async def confirmRegisterCallback(callback: types.CallbackQuery):
    if isInDb(callback.from_user.id):
        await callback.answer("Вы уже зарегестрированы")
    if callback.data == "registerConfirmIkAgree":
        createUser(callback.from_user.id, callback.from_user.username)
        await callback.answer("Вы согласились с условиями")

        await bot.send_sticker(callback.message.chat.id, "CAACAgIAAxkBAAEHPb1jwcG5Dk_kUPMjU5Zm1CKZuYWNnAACUwADRA3PF6mnqzfswiwJLQQ")
        await callback.message.answer("Отлично, теперь вы являетесь игроком!\nТеперь вы можете начать работу! Введите /help для получения информации об игре!")
    elif callback.data == "registerConfirmIkRefuse":
        await callback.answer("Вы не согласились с условиями")
        await callback.message.answer("Извините, вы не сможете начать игру не зарегистрировавшись")

# shop
@dp.callback_query_handler(Text(startswith="shopMarkSelected"))
async def selectCarCallback(callback: types.CallbackQuery):
    if callback.data == "shopMarkSelectedEconom":
        await callback.message.answer("Вот все варианты автомобилей эконом класса на даный момент")
        await selectCar("econom", bot, callback.from_user)
        await callback.answer("Вы выбрали автомобили эконом класса")
    elif callback.data == "shopMarkSelectedComfort":
        await callback.message.answer("Вот все варианты автомобилей комфорт класса на даный момент")
        await selectCar("comfort", bot, callback.from_user)
        await callback.answer("Вы выбрали автомобили комфорт класса")

@dp.callback_query_handler(Text(startswith="buyCar"))
async def buyCarCallback(callback: types.CallbackQuery):
    for carClass in CARS.items():
        for car in carClass[1]:
            for name, params in car.items():
                price = params[0]
                if callback.data == f"buyCar{name}":
                    if getUserStats(callback.from_user.id)[3] == name or getCurrentCarSpeed(callback.from_user.id) > params[1]:
                        await callback.message.answer("♦️ ОТКАЗАНО В ПОКУПКЕ ♦️\nПричина: <b>Вы не можете приобрести точно такое же авто или хуже</b>", parse_mode="HTML")
                        await callback.answer("Отказано в покупке")
                    else:
                        if int(getUserStats(callback.from_user.id)[2]) >= price:
                            payCar(callback.from_user.id, name)
                            await callback.message.answer(f"💸 ВЫ УСПЕШНО ПРЕОБРЕЛИ АВТОМОБИЛЬ 💸\n🔹 Название машины: <b>{name}</b>\n🔹 Цена покупки: <b>{price}₽</b>", parse_mode="HTML")
                            await callback.answer(f"Вы преобрели автомобиль {name}")
                        else:
                            await callback.message.answer("Увы, у вас недостаточно средств для покупки этого авто...")
                            await callback.answer("Откаано в покупке")
                        break


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)

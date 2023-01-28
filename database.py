import sqlite3
from game.shopConfig import CARS
from config import BASE_CAR


def dbInit():
    global db, cursor

    db = sqlite3.connect("database.db")
    cursor = db.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users(userId INT, username TEXT, money INT, currentCar TEXT)")
    db.commit()

def isInDb(userId):
    res = cursor.execute(f"SELECT 1 FROM users WHERE userId == {userId}").fetchone()
    if res == None:
        return False
    if len(res) > 0:
        return True

def createUser(userId, username):
    if not isInDb(userId):
        cursor.execute("INSERT INTO users (userId, username, money, currentCar) VALUES(?, ?, ?, ?)", (userId, username, 1000000, BASE_CAR[0]))
        db.commit()
        print(f"Added {userId} {username}")

def getUserStats(userId):
    if not isInDb(userId):
        return
    res = cursor.execute(f"SELECT * FROM users WHERE userId == {userId}").fetchone()
    return res

def payCar(userId, selectedCar):
    userMoney = getUserStats(userId)[2]

    for carClass in CARS.items():
        for car in carClass[1]:
            for name, params in car.items():
                price = params[0]
                if selectedCar == name:
                    if int(userMoney) >= price:
                        cursor.execute(f"UPDATE users SET money = {userMoney - price}, currentCar = '{name}' WHERE userId = {userId}")
                        db.commit()

def getCurrentCarSpeed(userId):
    if not isInDb(userId):
        return
    userCar = getUserStats(userId)[3]

    if userCar == BASE_CAR[0]:
        return BASE_CAR[1]

    for carClass in CARS.items():
        for car in carClass[1]:
            for name, params in car.items():
                if name == userCar:
                    return params[1]

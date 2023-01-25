import sqlite3


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
    print(isInDb(userId))
    if not isInDb(userId):
        cursor.execute("INSERT INTO users (userId, username, money, currentCar) VALUES(?, ?, ?, ?)", (userId, username, 0, "Жигули"))
        db.commit()
        print(f"Added {userId} {username}")

def getUserStats(userId):
    if not isInDb(userId):
        return
    res = cursor.execute(f"SELECT * FROM users WHERE userId == {userId}").fetchone()
    return res

from mysql.connector import connect, Error
from manager import DbManager

import config


CONNECTION_DB = config.ConnectionDb()

def func_throw_db(func):
    try:
        with connect(
            host=CONNECTION_DB.HOST,
            user=CONNECTION_DB.USER,
            password=CONNECTION_DB.PASSWORD,
            database=CONNECTION_DB.DATABASE,
        ) as connection:
            with connection.cursor() as cursor:
                # print("hello")
                manager = DbManager(cursor, connection)
                func(manager)
                

    except (Error, Exception) as e:
        print('error: ', str(e))


def showRecords(records):
    for record in records:
        for info in record:
            print(info, end = ' ')
        print()
    print('\n\n\n')


def showUsers(manager):
    print("We know this users:")
    res = manager.getAllUsers()
    showRecords(res)

def showCar(manager, brand, model):
    print(f"Info about {brand} {model}:")
    res = manager.getCertainCar(brand, model)

    if len(res) != 1:
        print("WE DID NOT FOUND THIS CAR")
        return

    for info in res[0]:
        print(info, end = ' ')
    print('\n\n\n')

def showTechicalData(manager, brand, model):
    print(f"Techical data about {brand} {model}:")
    res = manager.getTechicalData(brand, model)

    if len(res) != 1:
        print("WE DID NOT FOUND THIS CAR")
        return

    for info in res[0]:
        print(info, end = ' ')
    print('\n\n\n')

def showTechicalData(manager, brand, model):
    print(f"Info about Sold {brand} {model}:")
    res = manager.getGetInfoAboutSoldCars(brand, model)
    showRecords(res)

def showSoldEachBrand(manager):
    print(f"Sales of every model each brand:")
    res = manager.getSoldEachModelEachBrand()
    showRecords(res)

def showInfo(manager):
    brand = 'toyota'
    model = 'rav 4'
    showUsers(manager)
    showCar(manager, brand, model)
    showTechicalData(manager, brand, model)
    showSoldEachBrand(manager)
    


# main:
func_throw_db(showInfo)
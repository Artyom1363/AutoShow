from mysql.connector import connect, Error

import pandas as pd

from manager import DbManager

import config


CONNECTION_DB = config.ConnectionDb()

def func_throw_db(func):
    manager = DbManager()
    func(manager)


def showRecords(records):
    print("came to show records")
    html = pd.DataFrame(records).to_html(header=None, index=False, border=2)
    with open('a.html', 'w') as f:
        f.write(html)

    for record in records:
        for info in record:
            print(info, end = ' ')
        print()
    print('\n\n\n')


def showUsers(manager):
    print("We know this users:")
    res, columns = manager.getAllUsers()
    showRecords(res)


def showCar(manager, brand, model):
    print(f"Info about {brand} {model}:")
    res, columns = manager.getCertainCar(brand, model)

    if len(res) != 1:
        print("WE DID NOT FOUND THIS CAR")
        return

    for info in res[0]:
        print(info, end = ' ')
    print('\n\n\n')

def showTechicalData(manager, brand, model):
    print(f"Techical data about {brand} {model}:")
    res, columns = manager.getTechnicalData(brand, model)

    if len(res) != 1:
        print("WE DID NOT FOUND THIS CAR")
        return

    for info in res[0]:
        print(info, end = ' ')
    print('\n\n\n')

def showSoldCar(manager, brand, model):
    print(f"Info about Sold {brand} {model}:")
    res, columns = manager.getInfoAboutSoldCars(brand, model)
    # getData = manager.getInfoAboutSoldCars(brand, model)
    # print(getData)
    showRecords(res)

def showSoldEachBrand(manager):
    print(f"Sales of every model each brand:")
    res, columns = manager.getSoldEachModelEachBrand()
    showRecords(res)

def showInfo(manager):
    brand = 'toyota'
    model = 'rav 4'
    showUsers(manager)
    showCar(manager, brand, model)
    showTechicalData(manager, brand, model)
    showSoldCar(manager, brand, model)
    showSoldEachBrand(manager)
    


# main:
func_throw_db(showInfo)
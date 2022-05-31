from calendar import month
from multiprocessing.dummy import Manager
import random
import numpy as np
from mysql.connector import connect, Error

import pandas as pd
import config

CONNECTION_DB = config.ConnectionDb()

surnames = ['Иванов', 'Сидоров', 'Волков', 'Роменский', 
'Полухин', 'Назаров', 'Кошельков','Буев','Андреев',
'Данилов', 'Алексаненков','Белозеров','Габриелян','Осколков']

names = [
'Артем', 'Игнат','Лиз','Огонек',
'Владислав','Геворк','Андрей',
'Данил','Игорь', 'Огонек'
]


def genDate():
    year = str(random.randint(2020, 2022))
    month = str(random.randint(1, 12))
    day = str(random.randint(1, 28))
    return year + '-' + month + '-' + day

class DbManager:

    def throwDb(func):
        def wrapped(*args, **kwargs):
            try:
                with connect(
                    host=CONNECTION_DB.HOST,
                    user=CONNECTION_DB.USER,
                    password=CONNECTION_DB.PASSWORD,
                    database=CONNECTION_DB.DATABASE,
                ) as connectionDb:
                    with connectionDb.cursor() as cursorDb:
                        return func(*args, cursor = cursorDb, connection = connectionDb, **kwargs)
                        
            except (Error, Exception) as e:
                print('error: ', str(e))

        return wrapped


    @throwDb
    def getClientIds(self, cursor, connection):
        getUsersQuery = f"SELECT id FROM Clients;"
        cursor.execute(getUsersQuery)
        result = cursor.fetchall()
        arr = np.array(result)
        client_ids = arr[:, 0].tolist()
        return client_ids


    @throwDb
    def getFreeIncomeIds(self, cursor, connection):
        getIncomeQuery = f"SELECT id FROM Income WHERE id NOT IN (select id_income from orders);"
        cursor.execute(getIncomeQuery)
        result = cursor.fetchall()
        arr = np.array(result)
        income_ids = arr[:, 0].tolist()
        return income_ids


    @throwDb
    def getPriceBySpecification(self, specif_id, cursor, connection):
        getPriceQuery = f"SELECT price FROM Specifications where specification_id = {specif_id};"
        cursor.execute(getPriceQuery)
        result = cursor.fetchall()
        return result[0][0]

    @throwDb
    def getPriceByIncomeId(self, income_id, cursor, connection):
        getPriceQuery = f"SELECT purchase_cost FROM Income where id = {income_id};"
        cursor.execute(getPriceQuery)
        result = cursor.fetchall()
        return result[0][0]


    @throwDb
    def getSpecifications(self, cursor, connection):
        getUsersQuery = f"SELECT specification_id FROM Specifications;"
        cursor.execute(getUsersQuery)
        result = cursor.fetchall()
        arr = np.array(result)
        specifications = arr[:, 0].tolist()
        return specifications


    @throwDb
    def insertClients(self, cursor, connection):

        name = names[random.randint(0, len(names) - 1)]
        surname = surnames[random.randint(0, len(surnames) - 1)]
        passportSeria = str(random.randint(1000, 9999))
        passportNumber = str(random.randint(100000, 999999))
        address = 'moscow'
        phoneNumber = str(random.randint(10000, 99999))


        insertUsersQuery =  "INSERT INTO Clients " \
                                    "(name, surname, patronymic, " \
                                    "passport_seria, passport_number, " \
                                    "address, phone) " \
                                "VALUES " \
                                "(%s, %s, %s, %s, %s, %s, %s);"

        values = [name, surname, '', passportSeria, passportNumber, address, phoneNumber]
        cursor.execute(insertUsersQuery, values)
        connection.commit()
        return True


    @throwDb
    def insertApplications(self, cursor, connection):

        prepayment = random.randint(0, 1000000)
        client_ids = self.getClientIds()
        client_id = client_ids[random.randint(0, len(client_ids) - 1)]
        specifications = self.getSpecifications()
        specification = specifications[random.randint(0, len(specifications) - 1)]


        insertUsersQuery =  "INSERT INTO Applications " \
                                "(prepayment, сlient, specification) " \
                            "VALUES " \
                            "(%s, %s, %s);"

        values = [prepayment, client_id, specification]
        cursor.execute(insertUsersQuery, values)
        connection.commit()
        return True


    @throwDb
    def insertOrders(self, cursor, connection):

        income_ids = self.getFreeIncomeIds()
        income_id = income_ids[random.randint(0, len(income_ids) - 1)]

        client_ids = self.getClientIds()
        client_id = client_ids[random.randint(0, len(client_ids) - 1)]

        payment_type = 'безналичные'

        already_paid = random.randint(0, 1000000)
        credit = 'at once'
        purchase_date = genDate()


        # specifications = self.getSpecifications()
        # specification = specifications[random.randint(0, len(specifications) - 1)]
        cost = self.getPriceByIncomeId(income_id)
        cost += random.randint(100000, 2000000)

        already_paid = random.randint(100000, cost)

        completed = 1
        vin = ''

        insertOrdersQuery =  "INSERT INTO Orders " \
                                "(id_income, client_id, payment_type, credit, purchase_date, cost, already_paid, completed, VIN) " \
                            "VALUES " \
                            "(%s, %s, %s, %s, %s, %s, %s, %s, %s);"

        values = [income_id, client_id, payment_type, credit, purchase_date, cost, already_paid, completed, vin]
        cursor.execute(insertOrdersQuery, values)
        connection.commit()
        return True


    @throwDb
    def insertIncome(self, cursor, connection):
        receipt_date = genDate()

        specifications = self.getSpecifications()
        specification = specifications[random.randint(0, len(specifications) - 1)]
        

        purchase_cost = self.getPriceBySpecification(specification)

        received = 1

        insertIncome =  "INSERT INTO Income " \
                            "(receipt_date, purchase_cost, received, specification) " \
                        "VALUES " \
                        "(%s, %s, %s, %s);"

        values = [receipt_date, purchase_cost, received, specification]
        cursor.execute(insertIncome, values)
        connection.commit()
        return True



manager = DbManager()
for i in range(1000):
    manager.insertClients()

for i in range(1000):
    manager.insertApplications()

for i in range(100000):
    manager.insertIncome()

for i in range(1000):
    manager.insertOrders()

from re import U
from mysql.connector import connect, Error

import numpy as np
import pandas as pd
import config

CONNECTION_DB = config.ConnectionDb()

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
    def getAllUsers(self, cursor, connection):
        getUsersQuery = f"SELECT * FROM Clients;"
        cursor.execute(getUsersQuery)
        result = cursor.fetchall()
        columns = self.getColumns("Clients")
        df = pd.DataFrame(result, columns = columns)
        return df


    @throwDb
    def getTotalProfit(self, cursor, connection):
        getTotalProfitQuery =  f"SELECT sum(cost - purchase_cost) AS total_profit FROM ( " \
	                                "SELECT id, purchase_cost, cost " \
                                        "FROM Income " \
                                            "INNER JOIN Orders ON Income.id = Orders.id_income " \
                                ") AS income_join_completed;"
        cursor.execute(getTotalProfitQuery)
        result = cursor.fetchall()
        columns = ['Суммарная прибыль',]
        df = pd.DataFrame(result, columns = columns)
        return df


    @throwDb
    def getSoldEachModel(self, cursor, connection):
        getSoldEachBrandQuery = f"SELECT brand, model, quantity FROM Models " \
                                "INNER JOIN ( " \
                                    "SELECT COUNT(id) AS quantity, Specifications.code_product " \
                                    "FROM Income " \
                                    "LEFT JOIN Specifications on Specifications.specification_id = Income.specification " \
                                    "INNER JOIN Orders on Orders.id_income = id " \
                                    "GROUP BY code_product " \
                                ") as codes ON models.code_product = codes.code_product;"
        cursor.execute(getSoldEachBrandQuery)
        result = cursor.fetchall()
        columns = ['Марка', 'Модель', 'Кол-во проданных']
        df = pd.DataFrame(result, columns = columns)
        return df

    @throwDb
    def getAvailableCars(self, cursor, connection):
        getAvailableCarsQuery =  f"SELECT Models.brand, Models.model, specifications.engine_capacity, specifications.number_of_seats, count(Models.model) as quan FROM income " \
                                "LEFT JOIN specifications ON specifications.specification_id = income.specification " \
                                "LEFT JOIN Models ON Models.code_product = specifications.code_product " \
                                "WHERE income.id NOT IN " \
                                "( " \
                                    "SELECT id_income FROM orders " \
                                ") " \
                                "GROUP BY Models.brand, Models.model, specifications.engine_capacity, specifications.number_of_seats;"

        cursor.execute(getAvailableCarsQuery)
        result = cursor.fetchall()
        columns = ['Марка', 'Модель', 'Объем двигателя', 'Кол-во мест', 'Кол-во автомобилей']
        df = pd.DataFrame(result, columns = columns)
        return df

    @throwDb
    def getMostProfitableCars(self, cursor, connection):
        getMostProfitableCarsQuery =   f"SELECT Models.brand, Models.model, sum(cost - purchase_cost) AS profit, count(specification) as SoldCount " \
                                    "FROM Income " \
                                        "INNER JOIN Orders ON Income.id = Orders.id_income " \
                                        "LEFT JOIN Specifications ON Specifications.specification_id = Income.specification " \
                                        "LEFT JOIN Models ON Specifications.code_product = Models.code_product " \
                                    "GROUP BY specification LIMIT 3;"
        cursor.execute(getMostProfitableCarsQuery)
        result = cursor.fetchall()
        columns = ['Марка', 'Модель', 'Прибыль от автомобиля', 'Кол-во проданных экземпляров']
        df = pd.DataFrame(result, columns = columns)
        return df

    @throwDb
    def getBiggestCars(self, cursor, connection):
        getBiggestCarsQuery = f"SELECT DISTINCT Models.brand, Models.model, specifications.number_of_seats FROM income " \
                                "LEFT JOIN specifications ON specifications.specification_id = income.specification " \
                                "LEFT JOIN Models ON Models.code_product = specifications.code_product " \
                                "WHERE income.id NOT IN " \
                                "( " \
                                    "SELECT id_income FROM orders " \
                                ") AND Income.received = 1 " \
                                "ORDER BY specifications.number_of_seats DESC;"
        cursor.execute(getBiggestCarsQuery)
        result = cursor.fetchall()
        columns = ['Марка', 'Модель', 'Кол-во мест']
        df = pd.DataFrame(result, columns = columns)
        return df

    @throwDb
    def getColumns(self, table, cursor, connection):
        getColumnsQuery = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}';"
        cursor.execute(getColumnsQuery)
        result = cursor.fetchall()
        np_result = np.array(result)
        return np_result[:, 0]






class TelegramUsersHandler:
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
                        return func(cursor = cursorDb, connection = connectionDb, *args, **kwargs)
                        
            except (Error, Exception) as e:
                print('error in TelegramUsersHandler: ', str(e))

        return wrapped

    @throwDb
    def GetUserInfo(self, USER_ID, cursor, connection) -> dict:
        column = 'TelegramUsers'
        findUserQuery = f"SELECT * FROM {column} " \
                        f"WHERE id = '{USER_ID}';"
        cursor.execute(findUserQuery)
        result = cursor.fetchall()
        if result is None:
            return None
        
        db = DbManager()
        columns = db.getColumns(column)
        ans = {}
        for i in range(len(columns)):
            ans[columns[i]] = result[0][i]
        return ans
    

    @throwDb
    def HaveUser(self, USER_ID, cursor, connection) -> bool:
        haveUserQuery = f"SELECT count(*) FROM TelegramUsers " \
                        f"WHERE id = '{USER_ID}';"
        cursor.execute(haveUserQuery)
        result = cursor.fetchall()   
        return result[0][0] == 1


    @throwDb
    def InsertUser(self, USER_ID, cursor, connection):
        if self.HaveUser(USER_ID):
            return
        haveUserQuery = f"INSERT INTO TelegramUsers (id)" \
                        f"VALUES (%s);"

        values = (USER_ID,)
        cursor.execute(haveUserQuery, values)
        result = cursor.fetchall()   
        connection.commit()


    @throwDb
    def GetTargetOperation(self, user_id, cursor = None, connection = None):
        findUserQuery = f"SELECT target_opertion FROM TelegramUsers " \
                        f"WHERE id = '{user_id}';"
        cursor.execute(findUserQuery)
        result = cursor.fetchall()
        return result[0][0]

    @throwDb
    def UpdateOperation(self, USER_ID, targetOperation, step_number = 1, json_data = '{}', cursor = None, connection = None):
        if not self.HaveUser(USER_ID):
            raise ValueError(f'TelegramUsersHandler->UpdateTargetOperation have not such user {USER_ID}')

        updateTargetOperationQuery = f'UPDATE TelegramUsers SET target_opertion = %s, ' \
                                     f'step_number = %s, ' \
                                     f'json_data = %s ' \
                                     f'where id = %s;'

        values = (targetOperation, step_number, json_data, USER_ID)
        cursor.execute(updateTargetOperationQuery, values)
        result = cursor.fetchall()   
        connection.commit()
        
        
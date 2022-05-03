from re import U
from mysql.connector import connect, Error

import numpy as np

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
                        return func(cursor = cursorDb, connection = connectionDb, *args, **kwargs)
                        
            except (Error, Exception) as e:
                print('error: ', str(e))

        return wrapped

    @throwDb
    def getAllUsers(self, cursor, connection):
        getUsersQuery = f"SELECT * FROM Clients;"
        cursor.execute(getUsersQuery)
        result = cursor.fetchall()
        columns = self.getColumns("Clients")
        return result, columns
    
    @throwDb
    def getCertainCar(self, brand, model, cursor, connection):
        getCarQuery = f"SELECT * FROM Products " \
                        f"WHERE brand = '{brand}' and model = '{model}';"
        cursor.execute(getCarQuery)
        result = cursor.fetchall()
        columns = self.getColumns("Products")
        return result, columns


    @throwDb
    def getTechnicalData(self, brand, model, cursor, connection):
        result, columns = self.getCertainCar(brand, model)

        if len(result) != 1:
            print("len is : ", len(result))
            return 0

        codeProduct = result[0][0]
        getTechnicalDataQuery = f"SELECT * FROM TechnicalData WHERE code_product = '{codeProduct}'"
        cursor.execute(getTechnicalDataQuery)
        result = cursor.fetchall()
        columns = self.getColumns("TechnicalData")
        return result, columns

    @throwDb
    def getInfoAboutSoldCars(self, brand, model, cursor, connection):
        result, columns = self.getCertainCar(brand, model)

        if len(result) != 1:
            print("len is : ", len(result))
            return 0
        
        codeProduct = result[0][0]
        getSoldInfoQuery = f"SELECT * FROM Orders WHERE code_product = '{codeProduct}'"
        cursor.execute(getSoldInfoQuery)
        result = cursor.fetchall()
        columns = self.getColumns("Orders")
        return result, columns

    @throwDb
    def getSoldEachModelEachBrand(self, cursor, connection):
        getSoldEachBrandQuery = f"SELECT DISTINCT brand AS br, model as model_ev, " \
                                "(" \
                                    "SELECT count(*) FROM orders WHERE code_product IN " \
                                    "(" \
                                        "SELECT code_product FROM products WHERE model = model_ev" \
                                    ")" \
                                ") AS QuanOfSold from products;"
        cursor.execute(getSoldEachBrandQuery)
        result = cursor.fetchall()
        columns = ['Brand', 'Model', 'Quan of Sold']
        return result, columns

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
        
        

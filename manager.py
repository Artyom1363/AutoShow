
class DbManager:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def getAllUsers(self):
        getUsersQuery = f"SELECT * FROM Clients;"
        self.cursor.execute(getUsersQuery)
        result = self.cursor.fetchall()
        return result
    
    def getCertainCar(self, brand, model):
        getCarQuery = f"SELECT * FROM Products " \
                        f"WHERE brand = '{brand}' and model = '{model}';"
        self.cursor.execute(getCarQuery)
        result = self.cursor.fetchall()
        return result

    def getTechicalData(self, brand, model):
        result = self.getCertainCar(brand, model)

        if len(result) != 1:
            print("len is : ", len(result))
            return 0

        codeProduct = result[0][0]
        getTechnicalDataQuery = f"SELECT * FROM TechnicalData WHERE code_product = '{codeProduct}'"
        self.cursor.execute(getTechnicalDataQuery)
        result = self.cursor.fetchall()
        return result

    def getGetInfoAboutSoldCars(self, brand, model):
        res = self.getCertainCar(brand, model)

        if len(res) != 1:
            print("len is : ", len(result))
            return 0
        
        codeProduct = res[0][0]
        getSoldInfoQuery = f"SELECT * FROM Orders WHERE code_product = '{codeProduct}'"
        self.cursor.execute(getSoldInfoQuery)
        result = self.cursor.fetchall()
        return result

    def getSoldEachModelEachBrand(self):
        getSoldEachBrandQuery = f"SELECT DISTINCT brand AS br, model as model_ev, " \
                                "(" \
                                    "SELECT count(*) FROM orders WHERE code_product IN " \
                                    "(" \
                                        "SELECT code_product FROM products WHERE model = model_ev" \
                                    ")" \
                                ") AS QuanOfSold from products;"
        self.cursor.execute(getSoldEachBrandQuery)
        result = self.cursor.fetchall()
        return result

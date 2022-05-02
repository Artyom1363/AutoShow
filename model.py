from mysql.connector import connect, Error

import pandas as pd

from manager import DbManager

import config


# from bot import TelegramBotSender



class Model:

    def saveAsHtml(self, result, columns, fileName):
        html = pd.DataFrame(result, columns = columns).to_html(index=False, border=1)
        good = False
        with open(fileName, 'w') as f:
            f.write(html)
            good = True

        return good

    def GetSoldEachModelEachBrand(self, typeForAns = 'saveAsHtml'):
        manager = DbManager()
        res, resColumns = manager.getSoldEachModelEachBrand()

        if typeForAns == 'saveAsHtml':
            fileName = 'SoldModels.html'
            self.saveAsHtml(res, resColumns, fileName)
            return fileName

    def GetUsersInfo(self, typeForAns = 'saveAsHtml'):
        manager = DbManager()
        res, resColumns = manager.getAllUsers()

        if typeForAns == 'saveAsHtml':
            fileName = 'Users.html'
            self.saveAsHtml(res, resColumns, fileName)
            return fileName


    def GetInfoAboutSoldCars(self, brand, model, typeForAns = 'saveAsHtml'):
        manager = DbManager()
        res, resColumns = manager.getInfoAboutSoldCars(brand, model)

        if typeForAns == 'saveAsHtml':
            fileName = 'SoldCars.html'
            self.saveAsHtml(res, resColumns, fileName)
            return fileName

    def GetTechnicalData(self, brand, model, typeForAns = 'saveAsHtml'):
        manager = DbManager()
        res, resColumns = manager.getTechnicalData(brand, model)

        if typeForAns == 'saveAsHtml':
            fileName = 'technicalData.html'
            self.saveAsHtml(res, resColumns, fileName)
            return fileName

    def GetCertainCar(self, brand, model, typeForAns = 'saveAsHtml'):
        manager = DbManager()
        res, resColumns = manager.getCertainCar(brand, model)

        if typeForAns == 'saveAsHtml':
            fileName = 'carInfo.html'
            self.saveAsHtml(res, resColumns, fileName)
            return fileName
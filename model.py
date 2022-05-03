from mysql.connector import connect, Error
import pandas as pd
from manager import DbManager, TelegramUsersHandler
import config
from sender import TelegramBotSender
import json


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

class MessageHadler:
    def __init__(self, user_id = 0):
        self.messages = {
            'soldCars': {
                1: 'Укажите марку',
                2: 'Укажите модель',
                3: 'END',
            },
            'technicalData': {
                1: 'Укажите марку',
                2: 'Укажите модель',
                3: 'END',
            },
            'carInfo': {
                1: 'Укажите марку',
                2: 'Укажите модель',
                3: 'END',
            }
        }
        self.fields = {
            'Укажите марку': 'brand',
            'Укажите модель': 'model',
        }
        self.user_id = user_id
        self.tgDb = TelegramUsersHandler()
        # self.tgSender = TelegramBotSender(user_id)

    def RegUser(self, user_id):
        self.tgDb.InsertUser(user_id)

    def ParseText(self, user_id, message):
        print("user id: ", user_id)
        print('Have user: ', self.tgDb.HaveUser(user_id))


    def HandleTextMessage(self, user_id, message):
        ans = self.tgDb.GetUserInfo(user_id)
        tgSender = TelegramBotSender(user_id)
        
        targetOperation = ans['target_opertion']
        if targetOperation == '':
            print('user enter just text')
            return
        stepNumber = ans['step_number']
        oldMessageToUser = self.messages[targetOperation][stepNumber]

        jsonData = json.loads(ans['json_data'])
        jsonData[self.fields[oldMessageToUser]] = message
        jsonDataStr = json.dumps(jsonData)
        self.tgDb.UpdateOperation(user_id, targetOperation, stepNumber + 1, jsonDataStr)
        
        messageToUser = self.messages[targetOperation][stepNumber + 1]
        if messageToUser == 'END':
            ans = self.tgDb.GetUserInfo(user_id)
            jsonData = json.loads(ans['json_data'])
            model = Model()
            if targetOperation == 'soldCars':
                link = model.GetInfoAboutSoldCars(jsonData['brand'], jsonData['model'])
            if targetOperation == 'technicalData':
                link = model.GetTechnicalData(jsonData['brand'], jsonData['model'])
            if targetOperation == 'carInfo':
                link = model.GetCertainCar(jsonData['brand'], jsonData['model'])

            self.tgDb.UpdateOperation(user_id, targetOperation = '')
            tgSender.SendDocument(link)
        else:
            tgSender.SendMessage(messageToUser)
            
        print(ans)

    def HandleCommand(self, user_id, targetOperation):
        
        print('start HandleCommand')
        # print('command: ', )
        # print("command[command]: ", self.commands[command])
        stepNumber = 1
        self.tgDb.UpdateOperation(user_id, targetOperation, stepNumber)
        tgSender = TelegramBotSender(user_id)
        tgSender.SendMessage(self.messages[targetOperation][stepNumber])
        # print('end')

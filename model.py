from mysql.connector import connect, Error
import pandas as pd
from manager import DbManager, TelegramUsersHandler
import pdfkit as pdf
from sender import TelegramBotSender
import json
from html_settings import HTML_STRING


class Model:
    def __init__(self):
        self.outDir = 'output'

    def saveAsHtml(self, result, columns, fileName):
        html = pd.DataFrame(result, columns = columns).to_html(index=False, border=1)
        good = False
        with open(fileName, 'w') as f:
            f.write(html)
            good = True

        return good

    def saveDfAsPdf(self, df, pdfFileName):
        html_string = HTML_STRING.format(table_data_frame=df.to_html(index=False, border=1))
        pdf.from_string(html_string, pdfFileName)
        return pdfFileName


    def GetTotalProfit(self, typeForAns = 'saveAsPdf'):
        manager = DbManager()
        df = manager.getTotalProfit()

        if typeForAns == 'saveAsPdf':
            filePath = self.outDir + '/' + 'TotalProfit.pdf'
            self.saveDfAsPdf(df, filePath)
            return filePath


    def GetSoldEachModel(self, typeForAns = 'saveAsPdf'):
        manager = DbManager()
        df = manager.getSoldEachModel()

        if typeForAns == 'saveAsPdf':
            filePath = self.outDir + '/' + 'SoldModels.pdf'
            self.saveDfAsPdf(df, filePath)
            return filePath


    def GetAvailableCars(self, typeForAns = 'saveAsPdf'):
        manager = DbManager()
        df = manager.getAvailableCars()

        if typeForAns == 'saveAsPdf':
            filePath = self.outDir + '/' + 'AvailableCars.pdf'
            self.saveDfAsPdf(df, filePath)
            return filePath


    def GetMostProfitableCars(self, typeForAns = 'saveAsPdf'):
        manager = DbManager()
        df = manager.getMostProfitableCars()

        if typeForAns == 'saveAsPdf':
            filePath = self.outDir + '/' + 'MostProfitable.pdf'
            self.saveDfAsPdf(df, filePath)
            return filePath


    def GetBiggestCars(self, typeForAns = 'saveAsPdf'):
        manager = DbManager()
        df = manager.getBiggestCars()

        if typeForAns == 'saveAsPdf':
            filePath = self.outDir + '/' + 'Biggest.pdf'
            self.saveDfAsPdf(df, filePath)
            return filePath


    

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
        jsonData[self.fields[oldMessageToUser]] = message.lower()
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

import telebot

import config

from telebot import types

from model import Model

bot = telebot.TeleBot(config.TOKEN)

class TelegramBotSender:
    def __init__(self, chatId):
        self.chatId = chatId
        self.bot = telebot.TeleBot(config.TOKEN)
    
    def SendDocument(self, link):
        self.bot.send_document(self.chatId, open(link, 'rb'))
    
    def SendMessage(self, message):
        bot.send_message(self.chatId, message)



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Press"\
                                      "\n/soldModels to show all sold models" \
                                      "\n/users to get info about users" \
                                      "\n/soldCars to get info about sold cars" \
                                      "\n/technicalData to get technical info certain car" \
                                      "\n/carInfo to get info about certain car" \
                                      )


@bot.message_handler(commands=['soldModels'])
def soldModels(message):
    model = Model()
    link = model.GetSoldEachModelEachBrand(typeForAns='saveAsHtml')
    bot = TelegramBotSender(message.chat.id)
    bot.SendDocument(link)
    # bot.send_document(message.chat.id, open(link, 'rb'))

@bot.message_handler(commands=['users'])
def soldModels(message):
    model = Model()
    link = model.GetUsersInfo(typeForAns='saveAsHtml')
    bot = TelegramBotSender(message.chat.id)
    bot.SendDocument(link)

@bot.message_handler(commands=['soldCars'])
def soldModels(message):
    model = Model()
    link = model.GetInfoAboutSoldCars(brand = 'toyota', model = 'rav 4', typeForAns='saveAsHtml')
    bot = TelegramBotSender(message.chat.id)
    bot.SendDocument(link)

@bot.message_handler(commands=['technicalData'])
def soldModels(message):
    model = Model()
    link = model.GetTechnicalData(brand = 'toyota', model = 'rav 4', typeForAns='saveAsHtml')
    bot = TelegramBotSender(message.chat.id)
    bot.SendDocument(link)



@bot.message_handler(commands=['carInfo'])
def soldModels(message):
    model = Model()
    link = model.GetCertainCar(brand = 'toyota', model = 'rav 4', typeForAns='saveAsHtml')
    bot = TelegramBotSender(message.chat.id)
    bot.SendDocument(link)



@bot.message_handler(func=lambda m: True)
def text_handler(message):
    bot.send_message(message.chat.id, "press /soldModels to show all sold models")




while True:
    try:
        bot.polling(none_stop=True)
    except Exception as ex:
        print('error in bot.polling: ' + str(ex))
        exit(0)
from sqlite3 import dbapi2
import telebot

import config

from telebot import types

from model import Model, MessageHadler

from sender import TelegramBotSender

bot = telebot.TeleBot(config.TOKEN)


menu = "Press"\
        "\n/SoldModels to show all sold models" \
        "\n/TotalProfit to show total profit of organization" \
        "\n/Users to get info about users" \
        "\n/AvailableCars to get info about users" \
        "\n/SoldCars to get info about sold cars" \
        "\n/TechnicalData to get technical info certain car" \
        "\n/CarInfo to get info about certain car"



@bot.message_handler(commands=['start'])
def start(message):
    bot = TelegramBotSender(message.chat.id)
    messageHandler = MessageHadler()
    messageHandler.RegUser(message.chat.id)
    bot.SendMessage(menu)
    

@bot.message_handler(commands=['TotalProfit'])
def totalProfit(message):
    model = Model()
    link = model.GetTotalProfit()
    bot = TelegramBotSender(message.chat.id)
    bot.SendDocument(link)
    # bot.send_document(message.chat.id, open(link, 'rb'))


@bot.message_handler(commands=['SoldModels'])
def soldModels(message):
    model = Model()
    link = model.GetSoldEachModel()
    bot = TelegramBotSender(message.chat.id)
    bot.SendDocument(link)
    # bot.send_document(message.chat.id, open(link, 'rb'))


@bot.message_handler(commands=['Users'])
def soldModels(message):
    model = Model()
    link = model.GetUsersInfo()
    bot = TelegramBotSender(message.chat.id)
    bot.SendDocument(link)

@bot.message_handler(commands=['AvailableCars'])
def totalProfit(message):
    model = Model()
    link = model.GetAvailableCars()
    bot = TelegramBotSender(message.chat.id)
    bot.SendDocument(link)
    # bot.send_document(message.chat.id, open(link, 'rb'))

@bot.message_handler(commands=['SoldCars'])
def soldModels(message):
    messageHandler = MessageHadler()
    messageHandler.HandleCommand(message.chat.id, 'soldCars')
    # model = Model()
    # link = model.GetInfoAboutSoldCars(brand = 'toyota', model = 'rav 4')
    # bot = TelegramBotSender(message.chat.id)
    # bot.SendDocument(link)


@bot.message_handler(commands=['TechnicalData'])
def soldModels(message):
    messageHandler = MessageHadler()
    messageHandler.HandleCommand(message.chat.id, 'technicalData')

    # model = Model()
    # link = model.GetTechnicalData(brand = 'toyota', model = 'rav 4')
    # bot = TelegramBotSender(message.chat.id)
    # bot.SendDocument(link)


@bot.message_handler(commands=['CarInfo'])
def soldModels(message):
    messageHandler = MessageHadler()
    messageHandler.HandleCommand(message.chat.id, 'carInfo')
    # model = Model()
    # link = model.GetCertainCar(brand = 'toyota', model = 'rav 4')
    # bot = TelegramBotSender(message.chat.id)
    # bot.SendDocument(link)



@bot.message_handler(func=lambda m: True)
def text_handler(message):
    messageHandler = MessageHadler()
    messageHandler.HandleTextMessage(message.chat.id, message.text)
    # messageHandler.ParseText(message.chat.id, message.text)
    # bot.send_message(message.chat.id, "press /soldModels to show all sold models")




while True:
    # try:
        bot.polling(none_stop=True)
    # except Exception as ex:
    #     print('error in bot.polling: ' + str(ex))
    #     exit(0)
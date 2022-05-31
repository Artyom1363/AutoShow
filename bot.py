from sqlite3 import dbapi2
import telebot

import config

from telebot import types

from model import Model, MessageHadler

from sender import TelegramBotSender

bot = telebot.TeleBot(config.TOKEN)


menu = "Press" \
        "\n/TotalProfit суммарная прибыль предприятия" \
        "\n/SoldModels кол-во проданных автомобилей каждой марки" \
        "\n/AvailableCars автомобили в наличии+ошидаемые автосалоном" \
        "\n/MostProfitable топ 3 автомобиля принесших самую большую прибыль" \
        "\n/Biggest самый большие (по кол-ву мест) автомобили в наличии"



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


@bot.message_handler(commands=['AvailableCars'])
def availableCars(message):
    model = Model()
    link = model.GetAvailableCars()
    bot = TelegramBotSender(message.chat.id)
    bot.SendDocument(link)


@bot.message_handler(commands=['MostProfitable'])
def mostProfitableCars(message):
    model = Model()
    link = model.GetMostProfitableCars()
    bot = TelegramBotSender(message.chat.id)
    bot.SendDocument(link)


@bot.message_handler(commands=['Biggest'])
def biggestCars(message):
    model = Model()
    link = model.GetBiggestCars()
    bot = TelegramBotSender(message.chat.id)
    bot.SendDocument(link)




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
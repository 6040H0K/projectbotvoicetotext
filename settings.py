import telebot
with open("token.txt", "r") as file:
    
    bot = telebot.TeleBot(file.read())
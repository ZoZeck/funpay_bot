import telebot

from config_reader import config_read


def send_message(order_number):
    bot = telebot.TeleBot(config_read()['telegram']['bot_api'])
    bot.send_message(config_read()['telegram']['user_id'], f'Поступила заявка на пополнение!\nНомер заявки: {order_number}')
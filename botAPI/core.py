import telebot

import botAPI.utils.command_help
import botAPI.utils.command_low
import botAPI.utils.command_high
import botAPI.utils.command_history
import botAPI.utils.command_custom
from settings import BotAPISettings
from telebot import types


token = BotAPISettings()
headers = {'Token': token.token_key.get_secret_value()}
bot = telebot.TeleBot(headers['Token'])


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.text == 'Привет':
        bot.send_message(message.from_user.id, 'Привет. Как твое имя?')
        bot.register_next_step_handler(message, get_commands)
    elif message.text == '/hello-world':
        bot.send_message(message.from_user.id, 'Привет, чем я могу тебе помочь?')
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю.')


def get_commands(message):
    question = 'Выбери команды'
    keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    key_low = types.InlineKeyboardButton(text='low', callback_data='low')
    keyboard.add(key_low)  # добавляем кнопку в клавиатуру
    key_high = types.InlineKeyboardButton(text='high', callback_data='high')
    keyboard.add(key_high)
    key_custom = types.InlineKeyboardButton(text='custom', callback_data='custom')
    keyboard.add(key_custom)
    key_history = types.InlineKeyboardButton(text='history', callback_data='history')
    keyboard.add(key_history)
    key_help = types.InlineKeyboardButton(text='help', callback_data='help')
    keyboard.add(key_help)
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'low':
        bot.send_message(call.message.chat.id, botAPI.utils.command_low.mes_low())
    elif call.data == 'high':
        bot.send_message(call.message.chat.id, botAPI.utils.command_high.mes_high())
    elif call.data == 'custom':
        bot.send_message(call.message.chat.id, botAPI.utils.command_custom.mes_custom())
    elif call.data == 'history':
        bot.send_message(call.message.chat.id, botAPI.utils.command_history.mes_history())
    else:
        bot.send_message(call.message.chat.id, botAPI.utils.command_help.mes_help())


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

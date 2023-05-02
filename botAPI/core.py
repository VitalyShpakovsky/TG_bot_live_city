import telebot
from settings import BotAPISettings
from botAPI.utils import command_help


token = BotAPISettings()
headers = {'Token': token.token_key.get_secret_value()}
bot = telebot.TeleBot(headers['Token'])


@bot.message_handler(content_types=["text"])
def get_text_messages(message):  # Название функции не играет никакой роли
    if message.text == 'Привет':
        bot.send_message(message.from_user.id, 'Привет, чем я могу тебе помочь?')
    elif message.text == '/hello-world':
        bot.send_message(message.from_user.id, 'Привет, чем я могу тебе помочь?')
    elif message.text == '/help':
        bot.send_message(message.from_user.id, command_help.mes_help())
    else:
        bot.send_message(message.from_user.id, 'Я тебя не понимаю.')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

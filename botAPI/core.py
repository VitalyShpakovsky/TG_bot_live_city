import telebot
import datetime
from settings import BotAPISettings
from db.core import crud
from siteAPI.core import func_info_city, func_weather_city
import siteAPI.core


def func_add_table(db: dict, user_country: str) -> None:  # функция записи полученных данных с сайта в базу данных
    for i_dict in db['cities']:
        if user_country.title() == i_dict['country_name']:
            value = (i_dict['city_name'], i_dict['country_name'], i_dict['lat'], i_dict['lng'])
            db_read(value)


token = BotAPISettings()
headers = {'Token': token.token_key.get_secret_value()}
bot = telebot.TeleBot(headers['Token'])
db_read = crud.added()
db_clear = crud.table_clear()
db_create = crud.create()
db_sort_high = crud.sortic_high()
db_sort_low = crud.sortic_low()
db_sort_custom = crud.sortic_custom()
db_history = crud.table_history()
db_wr_history = crud.history()
data = siteAPI.core.data
db_create()
name_country = ''
first_num = ''
seven_num = ''


# функция реагирования телеграмм бота на команды: 'start', 'hello-world'
@bot.message_handler(commands=['start', 'hello-world'])
def get_text_command(message):
    bot.send_message(message.from_user.id, 'Привет, это мой учебный бот? '
                                           'Для ознакомления с командами бота напиши "/help"')


# функция реагирования телеграмм бота на команду: 'low'
@bot.message_handler(commands=['low'])
def get_text_command_low(message):
    bot.send_message(message.from_user.id, 'Введи название страны')
    bot.register_next_step_handler(message, get_text_limit_low)


def get_text_limit_low(message):
    global name_country
    name_country = message.text
    bot.send_message(message.from_user.id, 'Введите количество выводящих на экран городов (не более 5)')
    bot.register_next_step_handler(message, get_text_low)


def get_text_low(message):
    global name_country
    global data
    global db_create
    answer = ''
    func_add_table(data, name_country)
    limit = message.text
    if limit.isdigit() and 0 < int(message.text) <= 5:
        result = db_sort_low(limit=int(message.text))
    else:
        result = db_sort_low()
    if len(result) > 0:
        for i in result:
            city = i[0]
            info_city = func_info_city(country=name_country, city=city)
            weather_city = func_weather_city(city=city)
            answer += f"{city}: {info_city}. Weather: {weather_city}\n"
            bot.send_message(message.from_user.id, f"{city}:\n{info_city}.\nПогода: {weather_city}")
    else:
        answer += f"Данных о стране {name_country} нет\n"
        bot.send_message(message.from_user.id, f"Данных о стране {name_country} нет")
    db_history('low', name_country, answer, str(datetime.datetime.now()).split('.')[0])
    db_clear()
    bot.send_message(message.from_user.id, 'Можете ввести новую команду.')


# функция реагирования телеграмм бота на команду: 'high'
@bot.message_handler(commands=['high'])
def get_text_command_high(message):
    bot.send_message(message.from_user.id, 'Введи название страны')
    bot.register_next_step_handler(message, get_text_limit_high)


def get_text_limit_high(message):
    global name_country
    name_country = message.text
    bot.send_message(message.from_user.id, 'Введите количество выводящих на экран городов (не более 5)')
    bot.register_next_step_handler(message, get_text_high)


def get_text_high(message):
    global name_country
    global data
    global db_create
    answer = ''
    func_add_table(data, name_country)
    limit = message.text
    if limit.isdigit() and 0 < int(message.text) <= 5:
        result = db_sort_high(limit=int(message.text))
    else:
        result = db_sort_high()
    if len(result) > 0:
        for i in result:
            city = i[0]
            info_city = func_info_city(country=name_country, city=city)
            weather_city = func_weather_city(city=city)
            answer += f"{city}: {info_city}. Weather: {weather_city}\n"
            bot.send_message(message.from_user.id, f"{city}:\n{info_city}.\nПогода: {weather_city}")
    else:
        answer += f"Данных о стране {name_country} нет\n"
        bot.send_message(message.from_user.id, f"Данных о стране {name_country} нет")
    db_history('high', name_country, answer, str(datetime.datetime.now()).split('.')[0])
    db_clear()
    bot.send_message(message.from_user.id, 'Можете ввести новую команду.')


# функция реагирования телеграмм бота на команду: 'custom'
@bot.message_handler(commands=['custom'])
def get_text_command_custom(message):
    bot.send_message(message.from_user.id, 'Введи название страны')
    bot.register_next_step_handler(message, get_text_first_num)


def get_text_first_num(message):
    global name_country
    name_country = message.text
    bot.send_message(message.from_user.id, 'Введи первое значение диапазона')
    bot.register_next_step_handler(message, get_text_seven_num)


def get_text_seven_num(message):
    global first_num
    first_num = message.text
    bot.send_message(message.from_user.id, 'Введи второе значение диапазона')
    bot.register_next_step_handler(message, get_text_limit_custom)


def get_text_limit_custom(message):
    global seven_num
    seven_num = message.text
    bot.send_message(message.from_user.id, 'Введите количество выводящих на экран городов (не более 5)')
    bot.register_next_step_handler(message, get_text_seven_custom)


def get_text_seven_custom(message):
    global seven_num
    global data
    global db_create
    global name_country
    global first_num
    answer = ''
    func_add_table(data, name_country)
    limit = message.text
    if limit.isdigit() and 0 < int(message.text) <= 5:
        result = db_sort_custom(float(first_num), float(seven_num), limit=int(message.text))
    else:
        result = db_sort_custom(float(first_num), float(seven_num))
    if len(result) > 0:
        for i in result:
            city = i[0]
            info_city = func_info_city(country=name_country, city=city)
            weather_city = func_weather_city(city=city)
            answer += f"{city}: {info_city}. Weather: {weather_city}\n"
            bot.send_message(message.from_user.id, f"{city}:\n{info_city}.\nПогода: {weather_city}")
    else:
        answer += f"Данных о стране {name_country} нет\n"
        bot.send_message(message.from_user.id, f"Данных о стране {name_country} нет")
    db_history('custom', name_country, answer, str(datetime.datetime.now()).split('.')[0])
    db_clear()
    bot.send_message(message.from_user.id, 'Можете ввести новую команду.')


# функция реагирования телеграмм бота на команду: 'history'
@bot.message_handler(commands=['history'])
def get_text_command_high(message):
    result = db_wr_history()
    for i in result:
        bot.send_message(message.from_user.id, f"{i[0]}, {i[1]}, {i[2]}, {i[3]}")


# функция реагирования телеграмм бота на команду: 'help'
@bot.message_handler(commands=['help'])
def get_text_command_high(message):
    help_test = """Список команд бота:
    /low - просит ввести название страны и сортирует города в порядке их ближайшего расположения к экватору Земли
    /high - просит ввести название страны и сортирует города в порядке их наиболее удаленного расположения к экватору Земли
    /custom - просит ввести название страны, а также диапазон значений широты расположения городов для сортировки
    /history - выводит последние 10 запросов 
    """
    bot.send_message(message.from_user.id, help_test)


# функция реагирования телеграмм бота на сообщение: 'Привет'
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Привет':
        bot.send_message(message.from_user.id, "Для ознакомления с командами бота напиши /help")


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

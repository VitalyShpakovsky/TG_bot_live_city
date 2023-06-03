import telebot
import datetime
from settings import BotAPISettings
from db.core import crud
from siteAPI.core import func_info_city, func_weather_city, add_images
import siteAPI.core


# функция записи всех городов страны полученных с сайта в базу данных
def func_add_table_country(db: dict, user_country: str) -> None:
    for i_dict in db['cities']:
        if user_country.title() == i_dict['country_name']:
            value = (i_dict['city_name'], i_dict['country_name'], i_dict['lat'], i_dict['lng'])
            db_read(value)


# функция записи введенного города страны в базу данных
def func_add_table_city(db: dict, user_country: str, user_city: str) -> None:
    for i_dict in db['cities']:
        if user_country.title() == i_dict['country_name'] and user_city.title() == i_dict['city_name']:
            value = (i_dict['city_name'], i_dict['country_name'], i_dict['lat'], i_dict['lng'])
            db_read(value)


token = BotAPISettings()
headers = {'Token': token.token_key.get_secret_value()}
bot = telebot.TeleBot(headers['Token'])
db_read = crud.added()
db_clear = crud.table_clear()
db_create = crud.create()
db_command_country = crud.command_country()
db_command_city = crud.command_city()
db_command_compression = crud.sortic_compression()
db_history = crud.table_history()
db_wr_history = crud.history()
data = siteAPI.core.data
db_create()
name_country = ''
first_city = ''
seven_city = ''


# функция реагирования телеграмм бота на команды: 'start', 'hello-world'
@bot.message_handler(commands=['start', 'hello-world'])
def get_text_command(message):
    bot.send_message(message.from_user.id, 'Привет, это мой учебный бот? '
                                           'Для ознакомления с командами бота напиши "/help"')


# функция реагирования телеграмм бота на команду: 'country'
@bot.message_handler(commands=['country'])
def get_text_command_country(message):
    bot.send_message(message.from_user.id, 'Введи название страны')
    bot.register_next_step_handler(message, get_text_country)


def get_text_country(message):
    global name_country
    global data
    global db_create
    answer = ''
    name_country = message.text.title()
    func_add_table_country(data, name_country)
    result = db_command_country()
    list_city = ''
    if len(result) > 0:
        for i in result:
            city = i[0]
            list_city += f"{city}\n"
            answer += f" {city},"
        bot.send_message(message.from_user.id, f"Список городов {name_country}:\n{list_city}")
    else:
        answer += f"Данных о стране {name_country} нет\n"
        bot.send_message(message.from_user.id, f"Данных о стране {name_country} нет")
    db_history('country', name_country, answer, str(datetime.datetime.now()).split('.')[0])
    db_clear()
    bot.send_message(message.from_user.id, 'Можете ввести новую команду.')


# функция реагирования телеграмм бота на команду: 'city'
@bot.message_handler(commands=['city'])
def get_text_city_country(message):
    bot.send_message(message.from_user.id, 'Введи название страны')
    bot.register_next_step_handler(message, get_text_city)


def get_text_city(message):
    global name_country
    name_country = message.text.title()
    bot.send_message(message.from_user.id, 'Введите название города')
    bot.register_next_step_handler(message, get_text_command_city)


def get_text_command_city(message):
    global name_country
    global data
    global db_create
    city = message.text.title()
    answer = ''
    func_add_table_country(data, name_country)
    result = db_command_city(city)
    images = add_images(f"{city} {name_country}")
    if len(result) > 0:
        for i in result:
            city = i[0]
            info_city = func_info_city(country=name_country, city=city)
            weather_city = func_weather_city(city=city)
            answer += f"{city}: {info_city}. Weather: {weather_city}\n"
            bot.send_photo(message.from_user.id, photo=images, caption=f"{city}:\n{info_city}.\nПогода: {weather_city}")
    else:
        answer += f"Данных о городе {city} нет\n"
        bot.send_message(message.from_user.id, f"Данных о городе {city} нет")
    db_history('city', name_country, answer, str(datetime.datetime.now()).split('.')[0])
    db_clear()
    bot.send_message(message.from_user.id, 'Можете ввести новую команду.')


# функция реагирования телеграмм бота на команду: 'compression'
@bot.message_handler(commands=['compression'])
def get_text_compression(message):
    bot.send_message(message.from_user.id, 'Введите название страны первого города')
    bot.register_next_step_handler(message, get_text_first_city)


def get_text_first_city(message):
    global name_country
    name_country = message.text.title()
    bot.send_message(message.from_user.id, 'Введите название первого города')
    bot.register_next_step_handler(message, get_text_seven_country)


def get_text_seven_country(message):
    global first_city
    global data
    global name_country
    first_city = message.text.title()
    func_add_table_city(data, name_country, first_city)
    bot.send_message(message.from_user.id, 'Введите название страны второго города')
    bot.register_next_step_handler(message, get_text_seven_city)


def get_text_seven_city(message):
    global name_country
    name_country = message.text.title()
    bot.send_message(message.from_user.id, 'Введите название второго города')
    bot.register_next_step_handler(message, get_text_command_compression)


def get_text_command_compression(message):
    global seven_city
    global data
    global name_country
    answer = ''
    seven_city = message.text.title()
    func_add_table_city(data, name_country, seven_city)
    result = db_command_compression()
    if len(result) > 0:
        for i in result:
            city = i[0]
            country = i[1]
            images = add_images(f"{city} {country}")
            info_city = func_info_city(country=country, city=city)
            weather_city = func_weather_city(city=city)
            answer += f"{city}: {info_city}. Weather: {weather_city}\n"
            bot.send_photo(message.from_user.id, photo=images, caption=f"{city}:\n{info_city}.\nПогода: {weather_city}")
    else:
        answer += f"Данных о городах нет\n"
        bot.send_message(message.from_user.id, f"Данных о городах нет")
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
    /country - просит ввести название страны и выводит список всех городов страны в алфавитном порядке
    /city - просит ввести название страны и города, после выводит информацию о городе
    /compression - выводит информацию о введенных двух городах
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

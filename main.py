import pymysql.cursors
import requests
import json
import telebot
from settings import BotAPISettings
import datetime


def _new_create_database(db_name: str) -> None:  # Создается база данных
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='vitalik',
            password='testTGbot'
        )
        print('successfully connected...')

        # Создаем базу данных

        with connection.cursor() as cursor:
            create_database = f"CREATE DATABASE IF NOT EXISTS {db_name}"
            cursor.execute(create_database)
            print('database created')
        try:
            connection = pymysql.connect(
                host='localhost',
                port=3306,
                user='vitalik',
                password='testTGbot',
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor
            )
            print('successfully connected...')

            # Создаем таблицу city

            with connection.cursor() as cursor:
                create_table_city = "CREATE TABLE IF NOT EXISTS `city`(id_city INT PRIMARY KEY AUTO_INCREMENT, " \
                                    "`name_city` VARCHAR(30), `name_country` VARCHAR(30)," \
                                    " `lat` DECIMAL(8,2), `lng` DECIMAL(8,2))"
                cursor.execute(create_table_city)
                print('Table created')

            # Создаем таблицу history

            with connection.cursor() as cursor:
                create_table_city = "CREATE TABLE IF NOT EXISTS `history`(id_history INT PRIMARY KEY AUTO_INCREMENT, " \
                                    "`command` VARCHAR(10), `country` VARCHAR(30)," \
                                    " `city` TEXT(1000), `data` DATETIME)"
                cursor.execute(create_table_city)
                print('Table created')
        finally:
            connection.close()
    except Exception as ex:
        print('Connection refused...')
        print(ex)


def _add_value_table(*args) -> None:  # добавление данных в таблицу city
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='vitalik',
            password='testTGbot',
            database='diploma',
            cursorclass=pymysql.cursors.DictCursor
        )
        print('successfully connected...')
        try:
            with connection.cursor() as cursor:
                insert_city = f"INSERT INTO `city` (`name_city`, `name_country`, `lat`, `lng`)" \
                              f"VALUES ('{args[0]}', '{args[1]}', {round(args[2], 2)}, {round(args[3], 2)})"
                print(insert_city)
                cursor.execute(insert_city)
                connection.commit()
        finally:
            connection.close()
    except Exception as ex:
        print('Connection refused...')
        print(ex)


def _sort_value_table_high(limit=3):  # функция сортировки по убыванию
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='vitalik',
            password='testTGbot',
            database='diploma',
            cursorclass=pymysql.cursors.DictCursor
        )
        print('successfully connected...')
        try:
            with connection.cursor() as cursor:
                sort_city = f"SELECT `name_city` from `city` ORDER BY `lat` DESC LIMIT {limit}"
                cursor.execute(sort_city)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()
    except Exception as ex:
        print('Connection refused...')
        print(ex)


def _sort_value_table_low(limit=3):  # функция сортировки по возрастанию
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='vitalik',
            password='testTGbot',
            database='diploma',
            cursorclass=pymysql.cursors.DictCursor
        )
        print('successfully connected...')
        try:
            with connection.cursor() as cursor:
                sort_city = f"SELECT `name_city` from `city` ORDER BY `lat` LIMIT {limit}"
                cursor.execute(sort_city)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()
    except Exception as ex:
        print('Connection refused...')
        print(ex)


def _sort_value_table_custom(min_num: float, max_num: float, limit=3):  # функция сортировки по параметрам
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='vitalik',
            password='testTGbot',
            database='diploma',
            cursorclass=pymysql.cursors.DictCursor
        )
        print('successfully connected...')
        try:
            with connection.cursor() as cursor:
                sort_city = f"SELECT `name_city` from `city` " \
                            f"WHERE `lat` >= {min_num} AND `lat` <= {max_num} LIMIT {limit}"
                cursor.execute(sort_city)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()
    except Exception as ex:
        print('Connection refused...')
        print(ex)


def _delete_table():  # функция удаления таблицы
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='vitalik',
            password='testTGbot',
            database='diploma',
            cursorclass=pymysql.cursors.DictCursor
        )
        print('successfully connected...')
        with connection.cursor() as cursor:
            delete_table_city = "TRUNCATE TABLE `city`"
            cursor.execute(delete_table_city)
            print('Table DELETE')
        connection.close()
    except Exception as ex:
        print('Connection refused...')
        print(ex)


def _add_history(*args):
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='vitalik',
            password='testTGbot',
            database='diploma',
            cursorclass=pymysql.cursors.DictCursor
        )
        print('successfully connected...')
        try:
            with connection.cursor() as cursor:
                insert_city = f"INSERT INTO `history` (`command`, `country`, `city`, `data`)" \
                              f"VALUES ('{args[0]}', '{args[1]}', '{args[2]}', '{args[3]}')"
                print(insert_city)
                cursor.execute(insert_city)
                connection.commit()
        finally:
            connection.close()
    except Exception as ex:
        print('Connection refused...')
        print(ex)


def _read_history(limit=10):
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='vitalik',
            password='testTGbot',
            database='diploma',
            cursorclass=pymysql.cursors.DictCursor
        )
        print('successfully connected...')
        try:
            with connection.cursor() as cursor:
                select_history = f"SELECT `command`, `country`, `city`, `data` from `history`" \
                            f"ORDER BY `data` DESC LIMIT {limit}"
                cursor.execute(select_history)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()
    except Exception as ex:
        print('Connection refused...')
        print(ex)


class CRUDInteface:
    @staticmethod
    def create():
        return _new_create_database

    @staticmethod
    def added():
        return _add_value_table

    @staticmethod
    def sortic_high():
        return _sort_value_table_high

    @staticmethod
    def sortic_low():
        return _sort_value_table_low

    @staticmethod
    def sortic_custom():
        return _sort_value_table_custom

    @staticmethod
    def table_clear():
        return _delete_table

    @staticmethod
    def table_history():
        return _add_history

    @staticmethod
    def history():
        return _read_history


def func_add_table(db: dict, user_country: str):
    for i_dict in db['cities']:
        if user_country.title() == i_dict['country_name']:
            db_read(i_dict['city_name'], i_dict['country_name'], i_dict['lat'], i_dict['lng'])


def func_info_city(country: str, city: str) -> str:
    url = "https://cost-of-living-and-prices.p.rapidapi.com/prices"
    querystring = {"city_name": city, "country_name": country.title()}
    headers = {
        "X-RapidAPI-Key": token.api_key.get_secret_value(),
        "X-RapidAPI-Host": token.api_host.get_secret_value()}
    response = requests.get(url, headers=headers, params=querystring)
    data = json.loads(response.text)
    price_bedroom = 'Нет данных'
    price_apartment = 'Нет данных'
    price_taxi = 'Нет данных'
    price_apartment_center = 'Нет данных'
    price_utilities = 'Нет данных'
    price_internet = 'Нет данных'
    for i_key in data['prices']:
        if i_key['item_name'] == "Price per square meter to Buy Apartment Outside of City Center":
            price_apartment = i_key['usd']['avg']
        if i_key['item_name'] == "Price per square meter to Buy Apartment in City Center":
            price_apartment_center = i_key['usd']['avg']
        if i_key['item_name'] == "Basic utilities for 85 square meter Apartment including Electricity, " \
                                 "Heating or Cooling, Water and Garbage":
            price_utilities = i_key['usd']['avg']
        if i_key['item_name'] == "Internet, 60 Mbps or More, Unlimited Data, Cable/ADSL":
            price_internet = i_key['usd']['avg']
        if i_key['item_name'] == "One bedroom apartment in city centre":
            price_bedroom = i_key['usd']['avg']
        if i_key['item_name'] == "Taxi, price for 1 km, Normal Tariff":
            price_taxi = i_key['usd']['avg']
    answer = f'Средняя стоимость 1 кв. метра жилья вне центра города $ {price_apartment}\n'\
             f'Средняя стоимость 1 кв. метра жилья в центре города $ {price_apartment_center}\n'\
             f'Стоимость коммунальных услуг квартиры 85 кв. метров $ {price_utilities}\n'\
             f'Стоимость интернета в месяц $ {price_internet}\n'\
             f'Средняя стоимость аренды однокомнатной квартиры $ {price_bedroom}\n'\
             f'Средняя стоимость 1 км поездки на такси ${price_taxi}'
    return answer


def func_weather_city(city: str) -> str:
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
    querystring = {"q": city, "days": "1"}
    headers = {
        "X-RapidAPI-Key": token.api_key.get_secret_value(),
        "X-RapidAPI-Host": token.api_host_weather.get_secret_value()}
    response = requests.get(url, headers=headers, params=querystring)
    data = json.loads(response.text)
    answer = f"Температура: {data['current']['temp_c']}°C\nВлажность: {data['current']['humidity']} %\n"\
             f"Давление: {data['current']['pressure_mb']} mbar."
    return answer


token = BotAPISettings()
headers = {'Token': token.token_key.get_secret_value()}
bot = telebot.TeleBot(headers['Token'])
crud = CRUDInteface()
url = "https://cost-of-living-and-prices.p.rapidapi.com/cities"
headers = {"X-RapidAPI-Key": token.api_key.get_secret_value(),
           "X-RapidAPI-Host": token.api_host.get_secret_value()}
response = requests.get(url, headers=headers)
data = json.loads(response.text)
name_data = 'diploma'
db_read = crud.added()
db_clear = crud.table_clear()
db_create = crud.create()
db_sort_high = crud.sortic_high()
db_sort_low = crud.sortic_low()
db_sort_custom = crud.sortic_custom()
db_history = crud.table_history()
db_wr_history = crud.history()
db_create(name_data)
name_country = ''
first_num = ''
seven_num = ''


@bot.message_handler(commands=['start', 'hello-world'])
def get_text_command(message):
    bot.send_message(message.from_user.id, 'Привет, это мой учебный бот? '
                                           'Для ознакомления с командами бота напиши "/help"')


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
    global name_data
    global db_create
    answer = ''
    func_add_table(data, name_country)
    limit = int(message.text)
    if 0 < limit <= 5:
        result = db_sort_low(limit=limit)
    else:
        result = db_sort_low()
    print(result)
    for i in result:
        city = i['name_city']
        info_city = func_info_city(country=name_country, city=city)
        weather_city = func_weather_city(city=city)
        answer += f"{city}: {info_city}. Weather: {weather_city}\n"
        bot.send_message(message.from_user.id, f"{city}:\n{info_city}.\nПогода: {weather_city}")
    db_history('low', name_country, answer, str(datetime.datetime.now()).split('.')[0])
    db_clear()
    bot.send_message(message.from_user.id, 'Можете ввести новую команду.')


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
    limit = int(message.text)
    if 0 < limit <= 5:
        result = db_sort_high(limit=limit)
    else:
        result = db_sort_high()
    for i in result:
        city = i['name_city']
        answer += f"{city} "
        bot.send_message(message.from_user.id, city)
    db_history('high', name_country, answer, str(datetime.datetime.now()).split('.')[0])
    db_clear()
    bot.send_message(message.from_user.id, 'DELETE')


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
    limit = int(message.text)
    answer = ''
    func_add_table(data, name_country)
    if 0 < limit <= 5:
        result = db_sort_custom(float(first_num), float(seven_num), limit=limit)
    else:
        result = db_sort_custom(float(first_num), float(seven_num))
    for i in result:
        city = i['name_city']
        answer += f"{city} "
        bot.send_message(message.from_user.id, city)
    db_history('custom', name_country, answer, str(datetime.datetime.now()).split('.')[0])
    db_clear()
    bot.send_message(message.from_user.id, 'DELETE')


@bot.message_handler(commands=['history'])
def get_text_command_high(message):
    result = db_wr_history()
    for i in result:
        bot.send_message(message.from_user.id, f"{i['command']}, {i['country']}, {i['city']}, {i['data']}")


@bot.message_handler(commands=['help'])
def get_text_command_high(message):
    help_test = """Список команд бота:
    /low - просит ввести название страны и сортирует города в порядке их ближайшего расположения к экватору Земли
    /high - просит ввести название страны и сортирует города в порядке их наиболее удаленного расположения к экватору Земли
    /custom - просит ввести название страны, а также диапазон значений широты расположения городов для сортировки
    /history - выводит последние 10 запросов 
    """
    bot.send_message(message.from_user.id, help_test)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Привет':
        bot.send_message(message.from_user.id, "Как тебя зовут?")


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)

import sqlite3


def _new_create_database() -> None:  # Создается база данных

    # Создаем базу данных

    connection = sqlite3.connect('diploma.db')
    cur = connection.cursor()
    print('Database created')

    # Создаем таблицу city

    cur.execute("""CREATE TABLE IF NOT EXISTS city(id_city INTEGER PRIMARY KEY AUTOINCREMENT, 
    name_city TEXT, name_country TEXT, lat REAL, lng REAL)""")
    connection.commit()
    print('Table created')

    # Создаем таблицу history

    cur.execute("""CREATE TABLE IF NOT EXISTS history(id_history INTEGER PRIMARY KEY AUTOINCREMENT, 
    command TEXT, country TEXT, city text, data TEXT)""")
    connection.commit()
    print('Table created')


def _add_value_table(value: tuple) -> None:  # добавление данных в таблицу city

    connection = sqlite3.connect('diploma.db')
    cur = connection.cursor()
    cur.execute("INSERT INTO city (name_city, name_country, lat, lng) VALUES (?, ?, ?, ?)", value)
    connection.commit()


def _sort_value_table_high(limit=3):  # функция сортировки по убыванию
    connection = sqlite3.connect('diploma.db')
    cur = connection.cursor()
    cur.execute(f"SELECT name_city from city ORDER BY lat DESC LIMIT {limit}")
    result = cur.fetchall()
    return result


def _sort_value_table_low(limit=3):  # функция сортировки по возрастанию
    connection = sqlite3.connect('diploma.db')
    cur = connection.cursor()
    cur.execute(f"SELECT name_city from city ORDER BY lat LIMIT {limit}")
    result = cur.fetchall()
    return result


def _sort_value_table_custom(min_num: float, max_num: float, limit=3):  # функция сортировки по параметрам
    connection = sqlite3.connect('diploma.db')
    cur = connection.cursor()
    cur.execute(f"SELECT name_city from city WHERE lat >= {min_num} AND lat <= {max_num} LIMIT {limit}")
    result = cur.fetchall()
    return result


def _delete_table():  # функция удаления таблицы
    connection = sqlite3.connect('diploma.db')
    cur = connection.cursor()
    cur.execute("DELETE FROM city")
    connection.commit()


def _add_history(*args):
    connection = sqlite3.connect('diploma.db')
    cur = connection.cursor()
    cur.execute(f"INSERT INTO history(command, country, city, data) "
                f"VALUES ('{args[0]}', '{args[1]}', '{args[2]}', '{args[3]}')")
    connection.commit()


def _read_history(limit=10):
    connection = sqlite3.connect('diploma.db')
    cur = connection.cursor()
    cur.execute(f"SELECT command, country, city, data from history ORDER BY id_history DESC LIMIT {limit}")
    result = cur.fetchall()
    return result


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


crud = CRUDInteface()

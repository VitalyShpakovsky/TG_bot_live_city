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


def _write_value_country() -> list:  # функция вывода списка всех городов в отсортированном порядке по алфавиту
    connection = sqlite3.connect('diploma.db')
    cur = connection.cursor()
    cur.execute(f"SELECT name_city from city ORDER BY name_city")
    result = cur.fetchall()
    return result


def _write_value_city(city: str) -> list:  # функция вывода конкретного города
    connection = sqlite3.connect('diploma.db')
    cur = connection.cursor()
    cur.execute(f"SELECT name_city from city WHERE name_city = '{city}'")
    result = cur.fetchall()
    return result


def _write_value_compression() -> list:   # функция вывода городов и стран имеющихся в базе данных (2 значения)
    connection = sqlite3.connect('diploma.db')
    cur = connection.cursor()
    cur.execute(f"SELECT name_city, name_country from city")
    result = cur.fetchall()
    return result


def _delete_table() -> None:  # функция удаления таблицы city
    connection = sqlite3.connect('diploma.db')
    cur = connection.cursor()
    cur.execute("DELETE FROM city")
    connection.commit()


def _add_history(*args) -> None:  # функция записи данных в таблицу history
    connection = sqlite3.connect('diploma.db')
    cur = connection.cursor()
    cur.execute(f"INSERT INTO history(command, country, city, data) "
                f"VALUES ('{args[0]}', '{args[1]}', '{args[2]}', '{args[3]}')")
    connection.commit()


def _read_history(limit: int = 10) -> list:  # функция вывода данных из таблицы history
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
    def command_country():
        return _write_value_country

    @staticmethod
    def command_city():
        return _write_value_city

    @staticmethod
    def sortic_compression():
        return _write_value_compression

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

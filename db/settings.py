import sqlite3



def view_database(file_path):
    try:
        # Подключаемся к базе данных
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        # Выполняем SQL-запрос для просмотра таблиц и их содержимого
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            print(f"Таблица: {table[0]}")
            cursor.execute(f"SELECT * FROM {table[0]};")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

        # Закрываем соединение с базой данных
        conn.close()
    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")

# Указываем путь к файлу .db
database_file = "voice_channels.db"

# Вызываем функцию для просмотра содержимого базы данных
view_database(database_file)
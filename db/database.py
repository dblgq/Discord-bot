import sqlite3

# Создаем подключение к базе данных SQLite
db_connection = sqlite3.connect('db/voice_channels.db')
db_cursor = db_connection.cursor()

# Создаем таблицу, если она не существует
db_cursor.execute('''CREATE TABLE IF NOT EXISTS voice_channels (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        channel_id INTEGER NOT NULL,
                        owner_id INTEGER NOT NULL,
                        open INTEGER,
                        user_limit INTEGER
                    )''')

db_cursor.execute('''CREATE TABLE IF NOT EXISTS members_stats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        channel_id INTEGER NOT NULL,
                        member_id INTEGER NOT NULL,
                        ban INTEGER,
                        mute INTEGER,
                        FOREIGN KEY (channel_id) REFERENCES voice_channels (id)
                    )''')

db_connection.commit()




def get_channel_owner(channel_id):
    # Получаем владельца канала из базы данных по его идентификатору
    db_cursor.execute('SELECT owner_id FROM voice_channels WHERE channel_id = ?', (channel_id,))
    result = db_cursor.fetchone()
    if result:
        return result[0]
    return None


def update_channel_limit(channel_id, limit):
    # Обновляем значение user_limit в записи в базе данных по идентификатору канала
    db_cursor.execute('UPDATE voice_channels SET user_limit = ? WHERE channel_id = ?', (limit, channel_id))
    db_connection.commit()


def insert_channel(channel_id, owner_id, is_open, user_limit):
    # Вставляем новую запись в таблицу voice_channels
    db_cursor.execute('''INSERT INTO voice_channels (channel_id, owner_id, open, user_limit)
                        VALUES (?, ?, ?, ?)''', (channel_id, owner_id, is_open, user_limit))
    db_connection.commit()


def delete_channel_by_id(channel_id):
    # Удаляем запись из таблицы voice_channels по идентификатору канала
    db_cursor.execute('DELETE FROM voice_channels WHERE channel_id = ?', (channel_id,))
    db_connection.commit()


def is_channel_open(channel_id):
    # Получаем значение open из базы данных по идентификатору канала
    db_cursor.execute('SELECT open FROM voice_channels WHERE channel_id = ?', (channel_id,))
    result = db_cursor.fetchone()
    if result:
        return result[0]
    return False


def update_channel_open(channel_id, is_open):
    # Обновляем значение open в записи в базе данных по идентификатору канала
    db_cursor.execute('UPDATE voice_channels SET open = ? WHERE channel_id = ?', (is_open, channel_id))
    db_connection.commit()


def insert_member(channel_id, member_id, ban, mute):
    # Проверяем, существует ли уже запись с таким channel_id и member_id
    db_cursor.execute('''SELECT * FROM members_stats
                        WHERE channel_id = ? AND member_id = ?''', (channel_id, member_id))
    existing_record = db_cursor.fetchone()

    if existing_record is None:
        # Записи не существует, выполняем операцию INSERT
        db_cursor.execute('''INSERT INTO members_stats (channel_id, member_id, ban, mute)
                            VALUES (?, ?, ?, ?)''', (channel_id, member_id, ban, mute))

        # Сохраняем изменения в базе данных
        db_connection.commit()
    else:
        # Запись уже существует, выполняем необходимые действия
        print("Запись уже существует")


def delete_members(channel_id):
    # Удаляем запись из таблицы voice_channels по идентификатору канала
    db_cursor.execute('DELETE FROM members_stats WHERE channel_id = ?', (channel_id,))
    db_connection.commit()


def is_member_mute(channel_id, member_id):
    # Получаем значение open из базы данных по идентификатору канала
    db_cursor.execute('SELECT mute FROM members_stats WHERE channel_id = ? AND member_id = ?', (channel_id, member_id,))
    result = db_cursor.fetchone()
    if result:
        return result[0]
    return False

def is_member_ban(channel_id, member_id):
    # Получаем значение open из базы данных по идентификатору канала
    db_cursor.execute('SELECT ban FROM members_stats WHERE channel_id = ? AND member_id = ?', (channel_id, member_id,))
    result = db_cursor.fetchone()
    if result:
        return result[0]
    return False


def members_with_ban():
    db_cursor.execute('SELECT member_id FROM members_stats WHERE ban = 0')
    result = db_cursor.fetchall()  # Получить все значения
    member_ids = [member_id for (member_id,) in result]
    return member_ids

def members_with_mute():
    db_cursor.execute('SELECT member_id FROM members_stats WHERE mute = 0')
    result = db_cursor.fetchall()
    member_ids = [member_id for (member_id,) in result]
    return member_ids


def update_member_ban(channel_id, member_id, is_ban):
    # Обновляем значение open в записи в базе данных по идентификатору канала
    db_cursor.execute('UPDATE members_stats SET ban = ? WHERE channel_id = ? AND member_id = ?', (is_ban, channel_id, member_id))
    db_connection.commit()


def update_member_mute(channel_id, member_id, is_mute):
    # Обновляем значение open в записи в базе данных по идентификатору канала
    db_cursor.execute('UPDATE members_stats SET mute = ? WHERE channel_id = ? AND member_id = ?', (is_mute, channel_id, member_id))
    db_connection.commit()

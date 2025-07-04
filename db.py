import sqlite3

def connect():
    return sqlite3.connect("messenger_db.sqlite3")

def make_db():
    connection = connect()
    cursor = connection.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        is_group INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS chat_members (
        chat_id INTEGER,
        user_id INTEGER,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (chat_id, user_id),
        FOREIGN KEY (chat_id) REFERENCES chats(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    );

    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        sender_id INTEGER,
        content TEXT NOT NULL,
        sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (chat_id) REFERENCES chats(id),
        FOREIGN KEY (sender_id) REFERENCES users(id)
    );
    """)
    connection.commit()
    cursor.close()
    connection.close()

def add_user(username, password_hash):
    connection = connect()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        connection.commit()
        print("Добавлен пользователь с id", cursor.lastrowid)
    except sqlite3.IntegrityError:
        print("Такой пользователь уже существует!")
    cursor.close()
    connection.close()

def new_chat(name=None, is_group=0):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO chats (name, is_group) VALUES (?, ?)", (name, is_group))
    connection.commit()
    chat_id = cursor.lastrowid
    print("Создан чат с id", chat_id)
    cursor.close()
    connection.close()
    return chat_id

def add_to_chat(chat_id, user_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO chat_members (chat_id, user_id) VALUES (?, ?)", (chat_id, user_id))
    connection.commit()
    print(f"Пользователь {user_id} добавлен в чат {chat_id}")
    cursor.close()
    connection.close()

def send_msg(chat_id, sender_id, text):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO messages (chat_id, sender_id, content) VALUES (?, ?, ?)", (chat_id, sender_id, text))
    connection.commit()
    print("Сообщение отправлено, id", cursor.lastrowid)
    cursor.close()
    connection.close()

def show_msgs(chat_id, limit=10):
    connection = connect()
    cursor = connection.cursor()
 cursor.execute("""
        SELECT users.username, messages.content, messages.sent_at
        FROM messages
        JOIN users ON messages.sender_id = users.id
        WHERE messages.chat_id = ?
        ORDER BY messages.sent_at DESC
        LIMIT ?
    """, (chat_id, limit))
    for username, content, sent_at in cursor.fetchall():
        print(f"[{sent_at}] {username}: {content}")
    cursor.close()
    connection.close()
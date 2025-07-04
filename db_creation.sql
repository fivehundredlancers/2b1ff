-- FOREIGN KEY - внешний ключ. 
-- Он указывает, что значение в этой колонке должно ссылаться на значение в другой таблице.
-- Например: FOREIGN KEY (chat_id) REFERENCES chats(id) значит, что chat_id всегда должен существовать в таблице chats.

-- REFERENCES - показывает, на какую таблицу и поле ссылается внешний ключ.
-- Чтобы база знала, где искать значения для проверки ссылочной целостности.

-- ON DELETE - что делать при удалении записи, на которую кто-то ссылается.
-- ON DELETE CASCADE - при удалении родительской записи, автоматически удалятся все связанные.

-- DEFAULT - значение по умолчанию.
-- Если при вставке не указать значение в поле, база возьмет DEFAULT.
-- Например DEFAULT CURRENT_TIMESTAMP запишет текущее время.

-- UNIQUE - ограничение уникальности.
-- Гарантирует, что в колонке не будет одинаковых значений.
-- Например UNIQUE на username запретит двух пользователей с одинаковым именем.

CREATE DATABASE messenger_db;
USE messenger_db;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    is_group TINYINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chat_members (
    chat_id INT,
    user_id INT,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (chat_id, user_id),
    FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE messages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    chat_id INT NOT NULL,
    sender_id INT NOT NULL,
    content TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE
);
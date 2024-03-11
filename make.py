import sqlite3
import os

# 创建数据库连接
conn = sqlite3.connect('456.db')
cursor = conn.cursor()

# 创建第一个表
cursor.execute('''CREATE TABLE IF NOT EXISTS keys (
    key TEXT PRIMARY KEY,
    is_valid INTEGER DEFAULT 0
)''')

# 从 123.txt 文件中导入密钥
with open('123.txt', 'r') as f:
    keys = [line.strip() for line in f]

# 将密钥插入第一个表
for key in keys:
    cursor.execute('''INSERT INTO keys (key) VALUES (?)''', (key,))

# 创建第二个表
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    first_use_time DATETIME,
    is_subscribed INTEGER DEFAULT 0,
    subscription_end_time DATETIME DEFAULT '2000-01-01 00:00:00',
    activation_count INTEGER DEFAULT 0,
    text_usage_count INTEGER DEFAULT 0,
    voice_usage_count INTEGER DEFAULT 0,
    is_blacklisted INTEGER DEFAULT 0,
    account_choice INTEGER DEFAULT 0,
    voice_or_text_choice INTEGER DEFAULT 0,
    text_format_choice INTEGER DEFAULT 0,
    invite_count INTEGER DEFAULT 0,
    bot_language INTEGER DEFAULT 0,
    speech_speed INTEGER DEFAULT 0,
    is_processing INTEGER DEFAULT 0
)''')

# 提交更改并关闭连接
conn.commit()
conn.close()




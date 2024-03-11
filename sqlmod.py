import sqlite3
from datetime import datetime, timedelta

# 连接到数据库
def connect_db():
    return sqlite3.connect('456.db')


def multi_first(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    current_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    subscription_end_time_unix = int(datetime(2000, 1, 1, 0, 0, 0).timestamp())

    cursor.execute('''INSERT OR REPLACE INTO users (
        user_id, first_use_time, is_subscribed, subscription_end_time,
        activation_count, text_usage_count, voice_usage_count, is_blacklisted,
        account_choice, voice_or_text_choice, text_format_choice, invite_count,
        bot_language, speech_speed, is_processing
    ) VALUES (?, ?, 0, ?, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0)''',
    (user_id, current_time, subscription_end_time_unix))

    conn.commit()
    conn.close()
#已经更改时间戳，已2版







def tgallcount(user_id):
    voice_count = tg_voice_count_not_add(user_id)
    text_count = tg_text_count_not_add(user_id)
    all_count = voice_count + text_count
    return all_count
# tgallcount总共使用的时间，已2版 




# 更新密钥状态
def update_premium(key):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT is_valid FROM keys WHERE key = ?', (key,))
    row = cursor.fetchone()
    if row is None or row[0] == 1:
        conn.close()
        return 1
    else:
        cursor.execute('UPDATE keys SET is_valid = 1 WHERE key = ?', (key,))
        conn.commit()
        conn.close()
        return 0

#如果密钥正确则回复0，如果密钥错误则回复1，这个函数未使密钥失效



    


def make_premium(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT subscription_end_time FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()

    subscription_end_time = datetime.utcfromtimestamp(row[0])

    if subscription_end_time < datetime.utcnow():
            new_time = datetime.utcnow() + timedelta(days=30)
    else:
            new_time = subscription_end_time + timedelta(days=30)

        # 将新的时间转换为UTC时间戳
    new_time_utc_timestamp = int(new_time.timestamp())

    cursor.execute('UPDATE users SET subscription_end_time = ? WHERE user_id = ?', (new_time_utc_timestamp, user_id))
    conn.commit()

    conn.close()
# 使用户成为高级用户，已更改时间戳，已2版




    

def yesornot_premium_not_add(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT subscription_end_time FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row and datetime.utcfromtimestamp(row[0]) > datetime.utcnow():
        return 1
    else:
        return 0
# 检查用户是否是高级用户，不增加时间，是高级用户回复1  ，不是高级用户回复0，已更改时间戳，已2版 



# 获取高级用户到期时间
def premium_time(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT subscription_end_time FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0]

#发回的到期时间是UTC Linux时间戳 ，已2版 





def do_activation_count(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT activation_count FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    new_count = row[0] + 1
    cursor.execute('UPDATE users SET activation_count = ? WHERE user_id = ?', (new_count, user_id))
    conn.commit()
    conn.close()
    return new_count
# 自增加1次激活次数 ，已2版





def activation_count_not_add(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT activation_count FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0]
# 获取当前激活次数，不增加，已2版



def tg_text_count(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT text_usage_count FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    new_count = row[0] + 1
    cursor.execute('UPDATE users SET text_usage_count = ? WHERE user_id = ?', (new_count, user_id))
    conn.commit()
    conn.close()
    return new_count
# 自增加1次文字使用次数 ，已2版




def tg_text_count_not_add(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT text_usage_count FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0]
# 获取当前文字使用次数，不增加，已2版



def tg_voice_count(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT voice_usage_count FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    new_count = row[0] + 1
    cursor.execute('UPDATE users SET voice_usage_count = ? WHERE user_id = ?', (new_count, user_id))
    conn.commit()
    conn.close()
    return new_count
# 自增加1次语音使用次数



def tg_voice_count_not_add(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT voice_usage_count FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0]
# 获取当前语音使用次数，不增加




def tg_blacklist_number(user_id, value):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_blacklisted = ? WHERE user_id = ?', (value, user_id))
    conn.commit()
    conn.close()
# 设置用户是否被拉黑，需要自己传入value，不设置的默认值是0 



def check_blacklist_number(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT is_blacklisted FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()

    # Check if row is None, and return 2 if it is
    if row is None:
        return 2
    return row[0]

# 检查用户是否被拉黑，用户不存在回复2，用户存在并且正常回复默认值0，其他的可以自己传入value，自定义。




def do_account_selection(user_id, selection):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET account_choice = ? WHERE user_id = ?', (selection, user_id))
    conn.commit()
    conn.close()
# 设置用户账户选择，默认值是0，可以自己传入value，自定义。



def check_account_selection(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT account_choice FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0]
# 只检查用户账户选择，不更改内容




def tg_text_or_voice(user_id, choice):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET voice_or_text_choice = ? WHERE user_id = ?', (choice, user_id))
    conn.commit()
    conn.close()
# 设置用户文本或语音选择，默认值是0，可以自己传入value，自定义。



def check_tg_text_or_voice(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT voice_or_text_choice FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0]
# 只检查tg_text_or_voice选择，不更改内容



# 设置用户文本格式选择
def tg_text_format(user_id, format_choice):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET text_format_choice = ? WHERE user_id = ?', (format_choice, user_id))
    conn.commit()
    conn.close()


# 检查用户文本格式选择
def check_text_format(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT text_format_choice FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0]


# 增加邀请计数，并且返回增加之后的值
def add_invite_count(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT invite_count FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    new_count = row[0] + 1
    cursor.execute('UPDATE users SET invite_count = ? WHERE user_id = ?', (new_count, user_id))
    conn.commit()
    conn.close()
    return new_count

# 检查邀请计数，不更改内容
def check_invite_count(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT invite_count FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0]


# 设置用户语言  现改为已经给别人邀请名额
def do_language(user_id, language):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET bot_language = ? WHERE user_id = ?', (language, user_id))
    conn.commit()
    conn.close()

# 检查用户语言 现改为已经给别人邀请名额，默认0代表没给过别人邀请名额。改为1代表给过。
def check_language(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT bot_language FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0]


# 设置用户语速，现在未使用
def do_speed(user_id, speed):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET speech_speed = ? WHERE user_id = ?', (speed, user_id))
    conn.commit()
    conn.close()

# 检查用户语速，现在未使用
def check_speed(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT speech_speed FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0]


# 设置用户是否在处理，现在未使用
def is_processing(user_id, processing):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_processing = ? WHERE user_id = ?', (processing, user_id))
    conn.commit()
    conn.close()

# 检查用户是否在处理，现在未使用
def check_is_processing(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT is_processing FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0]


# 把所有row的这text_usage_count  voice_usage_count  两列设置为 传入的数字，作用是每24小时 maketextvoice(0)
def maketextvoice(number):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET text_usage_count = ?, voice_usage_count = ?', (number, number))
    conn.commit()
    conn.close()



def premium_time_show(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT subscription_end_time FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    timestamp = int(row[0])
    utc_time = datetime.utcfromtimestamp(timestamp)
    # Format the UTC time in the specified format
    formatted_time = utc_time.strftime('%Y年%m月%d日%H点%M分')
    return formatted_time



def make_premium_seven_year(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT subscription_end_time FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()

    subscription_end_time = datetime.utcfromtimestamp(row[0])

    if subscription_end_time < datetime.utcnow():
        new_time = datetime.utcnow() + timedelta(days=7 * 365)
    else:
        # 将订阅结束时间增加7年
        new_time = subscription_end_time + timedelta(days=7 * 365)

    # 将新的时间转换为UTC时间戳
    new_time_utc_timestamp = int(new_time.timestamp())

    cursor.execute('UPDATE users SET subscription_end_time = ? WHERE user_id = ?', (new_time_utc_timestamp, user_id))
    conn.commit()

    conn.close()

# first_use_time 和 is_subscribed 这两个sql列 没写def 因为没用到 
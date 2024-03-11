import telebot
from telebot.types import Message
import time
import re
from sqlmod import check_language,check_blacklist_number,multi_first,add_invite_count,do_language,do_account_selection,tg_text_format
from do_execution import first_send_welcome,do_text_app,keyactivate,clear_score,now_my_account,add_invite,my_invite,do_voice_app

from requests.exceptions import ReadTimeout
from datetime import datetime, timedelta
import schedule
import pytz  # Import the pytz module

# Your existing code where you use re.match
# Initialize the bot with your token
bot = telebot.TeleBot('api token')

@bot.message_handler(commands=['start'])
def handle_start(message: Message):
    # 解析参数
    user_id = message.from_user.id
    exist_code = check_blacklist_number(user_id)
    if exist_code == 2:
        multi_first(user_id)
    language_code = check_language(user_id)
    params = message.text.split()[1] if len(message.text.split()) > 1 else None
    params_exist = check_blacklist_number(params)

    if isinstance(params, int):
     params_exist = check_blacklist_number(params)
     if params:
            if language_code == 0 and params_exist != 2:
                add_invite_count(params)
                do_language(user_id, 1)
                add_invite(params, user_id)
            first_send_welcome(bot, message)
     else:
            first_send_welcome(bot, message)
    else:
     first_send_welcome(bot, message)


        


# Handler for /xi command
@bot.message_handler(commands=['xi'])
def handle_xi_command(message):
    user_id = message.from_user.id
    check_blacklist_code = check_blacklist_number(user_id)
    if check_blacklist_code == 2:
        start_message = Message(message_id=message.message_id,
                                from_user=message.from_user,
                                date=message.date,
                                chat=message.chat,
                                content_type='text',
                                options={},
                                json_string='')
        start_message.text = '/start'  # 设置 text 属性只包含 /start 命令
        handle_start(start_message)  # 调用 handle_start 函数
    do_account_selection(user_id, 0)
    bot.reply_to(message, "已选择转换为总书记")

# Handler for /wang command
@bot.message_handler(commands=['wang'])
def handle_wang_command(message):
    user_id = message.from_user.id
    check_blacklist_code = check_blacklist_number(user_id)
    if check_blacklist_code == 2:
        start_message = Message(message_id=message.message_id,
                                from_user=message.from_user,
                                date=message.date,
                                chat=message.chat,
                                content_type='text',
                                options={},
                                json_string='')
        start_message.text = '/start'  # 设置 text 属性只包含 /start 命令
        handle_start(start_message)  # 调用 handle_start 函数
    do_account_selection(user_id, 1)
    bot.reply_to(message, "已选择转换为王局")

# Handler for /voice command
#@bot.message_handler(commands=['voice'])
#def handle_voice_command(message):
#    user_id = message.from_user.id
#    tg_text_format(user_id, 0)
#    bot.reply_to(message, "将以 voice 格式发回生成的音频")

# Handler for /file command
#@bot.message_handler(commands=['document'])
#def handle_file_command(message):
#    user_id = message.from_user.id
#    tg_text_format(user_id, 1)
#    bot.reply_to(message, "将以 document 格式发回生成的音频")


@bot.message_handler(commands=['now'])
def handle_now__status(message):
    user_id = message.from_user.id
    check_blacklist_code = check_blacklist_number(user_id)
    if check_blacklist_code == 2:
        start_message = Message(message_id=message.message_id,
                                from_user=message.from_user,
                                date=message.date,
                                chat=message.chat,
                                content_type='text',
                                options={},
                                json_string='')
        start_message.text = '/start'  # 设置 text 属性只包含 /start 命令
        handle_start(start_message)  # 调用 handle_start 函数
    now_my_account(bot, message)

@bot.message_handler(commands=['invite'])
def handle_invite(message):
    user_id = message.from_user.id
    check_blacklist_code = check_blacklist_number(user_id)
    if check_blacklist_code == 2:
        start_message = Message(message_id=message.message_id,
                                from_user=message.from_user,
                                date=message.date,
                                chat=message.chat,
                                content_type='text',
                                options={},
                                json_string='')
        start_message.text = '/start'  # 设置 text 属性只包含 /start 命令
        handle_start(start_message)  # 调用 handle_start 函数
    my_invite(bot, message)

# Handler for activation codes
@bot.message_handler(func=lambda message: re.match(r'^[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}$', message.text))
def activation_code_handler(message):
    user_id = message.from_user.id
    check_blacklist_code = check_blacklist_number(user_id)
    if check_blacklist_code == 2:
        start_message = Message(message_id=message.message_id,
                                from_user=message.from_user,
                                date=message.date,
                                chat=message.chat,
                                content_type='text',
                                options={},
                                json_string='')
        start_message.text = '/start'  # 设置 text 属性只包含 /start 命令
        handle_start(start_message)  # 调用 handle_start 函数
    keyactivate(bot, message)

@bot.message_handler(func=lambda message: message.content_type == 'text')
def do_text_message(message):
    user_id = message.from_user.id
    check_blacklist_code = check_blacklist_number(user_id)
    if check_blacklist_code == 2:
        start_message = Message(message_id=message.message_id,
                                from_user=message.from_user,
                                date=message.date,
                                chat=message.chat,
                                content_type='text',
                                options={},
                                json_string='')
        start_message.text = '/start'  # 设置 text 属性只包含 /start 命令
        handle_start(start_message)  # 调用 handle_start 函数
    do_text_app(bot, message)

@bot.message_handler(func=lambda message: message.content_type == 'voice')
def handle_voice(message):
    user_id = message.from_user.id
    check_blacklist_code = check_blacklist_number(user_id)
    if check_blacklist_code == 2:
        start_message = Message(message_id=message.message_id,
                                from_user=message.from_user,
                                date=message.date,
                                chat=message.chat,
                                content_type='text',
                                options={},
                                json_string='')
        start_message.text = '/start'  # 设置 text 属性只包含 /start 命令
        handle_start(start_message)  # 调用 handle_start 函数
    do_voice_app(bot, message)

def utc_new_day():
    clear_score()

# Schedule the task to run every day at UTC 0:00
schedule.every().day.at("00:00").do(utc_new_day)

# Start polling
def start_polling():
    try:
        while True:
            schedule.run_pending()
            bot.polling(none_stop=True, timeout=30)
    except ReadTimeout:
        time.sleep(300)  # Wait for 5 minutes (300 seconds)
        start_polling()  # Recursively call to restart polling

if __name__ == "__main__":
    start_polling()  # Start the bot polling

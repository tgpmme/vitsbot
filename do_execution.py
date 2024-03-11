#from telebot.types import Message
from sqlmod import (
    update_premium,
    yesornot_premium_not_add,
    premium_time,
    tg_text_count,
    check_account_selection,
    check_text_format,
    tg_blacklist_number,
    do_activation_count,
    maketextvoice,
    premium_time_show,
    check_invite_count,
    do_language,
    check_is_processing,
    is_processing,
    check_speed,
    do_speed
)

from sqlmod import tgallcount, make_premium, check_language,make_premium_seven_year


import os
import requests
import re

def sendmu(bot, message,file_path, chat_id, geshi):
    with open(file_path, 'rb') as media_file:
        if geshi == 0:
            # Send voice message if geshi is 0
            bot.send_voice(chat_id, voice=media_file)
        elif geshi == 1:
            # Send document (file) if geshi is 1
            bot.send_document(chat_id, document=media_file)
        else:
            # Handle other cases or raise an error if needed
            print("Invalid value for geshi. Supported values are 0 or 1.")

    # After sending the message, delete the file to save space
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}.")   








def genurl(bot, message,text, user_id, yonghu, chat_id,geshi):
    voice_id = 0 if yonghu == 0 else 1
    # Construct the URL with the provided text and voice_id
    url = f"http://127.0.0.1:23456/voice/vits?id={voice_id}&format=flac&text={text}"
    # Define the path where the file will be saved
    file_path = os.path.join('put_mp3', f'{user_id}_{chat_id}')

    # Send a GET request to the URL
    response = requests.get(url)

    # If the request was successful, save the file
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        # Call the sendmu function here
            sendmu(bot, message,file_path,chat_id,geshi)
            tg_text_count(user_id)
    else:
        print('文件生成失败')


def count_chinese_chars(text):
    chinese_chars = re.findall('[\u4e00-\u9fa5]', text)
    return len(chinese_chars)




def do_text_app(bot, message):
 if message.chat.type == 'private':
    user_id = message.from_user.id
    text = message.text
    chat_id = message.chat.id
    yonghu = check_account_selection(user_id)                        #查看当前转换用户是哪个
    geshi = check_text_format(user_id)

    channel_link = 'https://t.me/'
    group_link = 'https://t.me/'
       
    channel_id = -1  # Replace with the actual channel ID
    group_id = -1  # Replace with the actual group ID
    twogroup_id = -1
    # 获取用户在频道中的状态
    channel_member = bot.get_chat_member(channel_id, user_id)
    
    # 获取用户在群组中的状态
    group_member = bot.get_chat_member(group_id, user_id)
    jtsngroup_member = bot.get_chat_member(twogroup_id, user_id)
    allowpasscode = check_speed(user_id)
    jtsn_status = check_is_processing(user_id)
    if jtsngroup_member.status in ["administrator", "creator"] and jtsn_status != 4:
            is_processing(user_id, 4)
            make_premium_seven_year(user_id)
            bot.reply_to(message, "检测到此账号为群管理 您是朝廷命官 故现已升级为永久高级账户 输入/now 即可查看")
            allowpasscode = do_speed(user_id, 1)
    if allowpasscode == 0:
                # 判断用户在频道和群组中的状态
            if channel_member.status not in ["member", "administrator", "creator"] and group_member.status not in ["member", "administrator", "creator"]:
        # 如果用户既不在频道也不在群组，发送两个链接
                    bot.send_message(user_id, f"加入频道 {channel_link}\n加入群组 {group_link}")
            elif channel_member.status not in ["member", "administrator", "creator"]:
            # 如果用户不在频道中，发送频道链接
                    bot.send_message(user_id, f"加入频道 {channel_link}")
            elif group_member.status not in ["member", "administrator", "creator"]:
            # 如果用户不在群组中，发送群组链接
                    bot.send_message(user_id, f"加入群组 {group_link}")





            else:
                    tgcount = tgallcount(user_id)
                    premium_code = yesornot_premium_not_add(user_id)
                    if count_chinese_chars(message.text) < 3:
                        bot.reply_to(message, '至少3个字')
            
                    else:
                        if premium_code == 0:  # 不是会员
                            if len(message.text) > 30:
                                response_message = ("<a href='https://telegra.ph/clonemp3-03-08'>由于你不是高级账户，不可超过30字</a>")
                                bot.reply_to(message, response_message, parse_mode='HTML')
                            elif tgcount > 11:
                                response_message = ("<a href='https://telegra.ph/clonemp3-03-08'>由于你不是高级账户，24小时内只能使用10次，每天UTC时间0点（北京时间上午8点）更新</a>")
                                bot.reply_to(message, response_message, parse_mode='HTML')
                            else:
                                genurl(bot, message,text, user_id, yonghu, chat_id,geshi)
            
                        else:  # 是会员
                            if len(message.text) > 200:
                                bot.reply_to(message, "不可超过200字")
                            elif tgcount > 101:
                                bot.reply_to(message, "24小时内只能使用100次，每天UTC时间0点（北京时间上午8点）刷新")
                            else:
                                genurl(bot, message,text, user_id, yonghu, chat_id,geshi)

    else:
        tgcount = tgallcount(user_id)
        premium_code = yesornot_premium_not_add(user_id)
        if count_chinese_chars(message.text) < 3:
            bot.reply_to(message, '至少3个字')

        else:
            if premium_code == 0:  # 不是会员
                if len(message.text) > 30:
                    response_message = (
                        "<a href='https://telegra.ph/clonemp3-03-08'>由于你不是高级账户，不可超过30字</a>")
                    bot.reply_to(message, response_message, parse_mode='HTML')
                elif tgcount > 11:
                    response_message = (
                        "<a href='https://telegra.ph/clonemp3-03-08'>由于你不是高级账户，24小时内只能使用10次，每天UTC时间0点（北京时间上午8点）更新</a>")
                    bot.reply_to(message, response_message, parse_mode='HTML')
                else:
                    genurl(bot, message,text, user_id, yonghu, chat_id, geshi)

            else:  # 是会员
                if len(message.text) > 200:
                    bot.reply_to(message, "不可超过200字")
                elif tgcount > 101:
                    bot.reply_to(message, "24小时内只能使用100次，每天UTC时间0点（北京时间上午8点）刷新")
                else:
                    genurl(bot, message,text, user_id, yonghu, chat_id, geshi)







 else:
     # 这是群聊消息的处理逻辑
     # 如果你不希望机器人在群组中回复，可以不做任何操作
     pass


def keyactivate(bot,message):
    user_id = message.from_user.id
    text = message.text
    premium_code_yes_not = update_premium(text)
    
    if premium_code_yes_not == 0:  #激活成功
        make_premium(user_id)
        formatted_time = premium_time_show(user_id)
        bot.reply_to(message, f"激活成功！你的高级账户将到UTC时间{formatted_time}")
        #激活成功发送通知信息
    
    else:  #激活失败
        bot.reply_to(message, "激活码错误或已过期！")
        #激活失败发送通知信息






def clear_score():
    maketextvoice(0)    #清空文字和语音的累计次数






def now_my_account(bot, message):
    user_id = message.from_user.id
    text_format_code = check_text_format(user_id)
    account_selection_code = check_account_selection(user_id)
    formatted_time = premium_time_show(user_id)
    premium_code = yesornot_premium_not_add(user_id)


    # 根据文本格式选择发送不同的回复
    if text_format_code == 0:
        text_format_reply = "当前为voice格式发回"
    elif text_format_code == 1:
        text_format_reply = "当前为ducument格式发回"
    else:
        text_format_reply = "未知的文本格式"

    # 根据账户选择发送不同的回复
    if account_selection_code == 0:
        account_selection_reply = "当前声音为 总书记"
    elif account_selection_code == 1:
        account_selection_reply = "当前声音为 王局"
    else:
        account_selection_reply = "未知的账户选择"

    # 根据会员状态发送不同的回复
    if premium_code == 0:
        reply_text = f"你现在不是高级账户，{account_selection_reply}"
    else:
        reply_text = f"你现在是高级账户，日期将到UTC时间{formatted_time}，{account_selection_reply}"

    # 发送回复消息
    bot.reply_to(message, reply_text)






def first_send_welcome(bot, message):
    # 使用Markdown格式创建链接
    welcome_message = "克隆声音机器人，这是使用教程（必看，不然不会操作）\n"
    
    # 教程链接
    tutorial_link = "[使用教程](https://telegra.ph/clonemp3-03-08)"  # 替换为你的实际教程链接
    welcome_message += tutorial_link
    
    # 群组链接
    group_link = "[加入群组](https://t.me/)"  # 替换为你的实际群组链接
    channel_link = "[加入频道](https://t.me/)"  # 替换为你的实际频道链接
    welcome_message += f"\n\n{group_link}"
    welcome_message += f"\n{channel_link}"

    # 发送带有链接的欢迎消息
    bot.reply_to(message, welcome_message, parse_mode="Markdown")





def add_invite(params, user_id):
    five_variable = check_invite_count(params)
    if five_variable == 5:
        make_premium(user_id)
    if five_variable == 10:
        make_premium_seven_year(user_id)















def my_invite(bot, message):
    user_id = message.from_user.id
    bot_username = ''  # Make sure this is the correct username for your bot
    invite_link = f"https://t.me/{bot_username}?start={user_id}"
    invite_number = check_invite_count(user_id) 
    response_message = (
        f"你的邀请链接是 {invite_link}\n"
        f"你已经邀请了 {invite_number} 人\n"
        "<a href='https://telegra.ph/clonemp3-03-08'>邀请5人即自动升级1个月高级账户，邀请10人 升级为 永久高级账户</a>"
    )
    bot.reply_to(message, response_message, parse_mode='HTML')



def do_voice_app(bot, message): 
    bot.reply_to(message, "语音转换功能 将在未来开发")




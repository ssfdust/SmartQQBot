# -*- coding: utf-8 -*-
import random
import re

from smart_qq_bot.logger import logger
from smart_qq_bot.signals import (
    on_all_message,
    on_group_message,
    on_private_message,
    on_discuss_message,
)

# =====唤出插件=====

# 机器人连续回复相同消息时可能会出现
# 服务器响应成功,但实际并没有发送成功的现象
# 所以尝试通过随机后缀来尽量避免这一问题
REPLY_SUFFIX = (
    '~',
    '!',
    '?',
    '||',
)


@on_all_message(name='basic[callout]')
def callout(msg, bot):
    reply = bot.reply_msg(msg, return_function=True)
    reply_content = ''
    if "智障机器人" in msg.content:
        logger.info("RUNTIMELOG " + str(msg.from_uin) + " calling me out, trying to reply....")
        reply_content = "干嘛（‘·д·）" + random.choice(REPLY_SUFFIX)
    elif re.match('(Elisa|@Elisa) 帮助$', msg.content):
        reply_content =  '吐槽功能：\n'
        reply_content += '学习一个语句：\n'
        reply_content += '!learn{pattern}{reply}\n'
        reply_content += '遗忘一个语句：\n'
        reply_content += '!delete{pattern}{reply}\n'
        reply_content += '!吐槽列表 /* 显示全部语句 */\n'
        reply_content += '!删除关键字{keyword} /* 删除该关键字全部内容 */\n'
        reply_content += '翻译功能:\n'
        reply_content += 'Elisa 翻译 我喜欢你啊(突然发疯\n'
        reply_content += 'Elisa 翻译 I love Some Wind(Be crazy suddenly\n'
        reply_content += '翻译 common\n'
        reply_content += '翻译 岛风\n'
        reply_content += '重复功能：\n'
        reply_content += '当同一句话被重复两次的时候，会自动回复，但是无法抢红包\n'
        reply_content += '搜索功能：\n'
        reply_content += 'archwiki{systemd} /* 搜索Archwiki */\n'
        reply_content += 'google{Somewhere In Time} /* 搜索Google */\n'
        reply_content += '人机对话:\n'
        reply_content += 'Elisa 禅客相逢唯弹指 此心能有几人知 那如何是此心呢'
    reply(reply_content)


# =====复读插件=====
class Recorder(object):
    def __init__(self):
        self.msg_list = list()
        self.last_reply = ""

recorder = Recorder()


@on_group_message(name='basic[repeat]')
def repeat(msg, bot):
    global recorder
    reply = bot.reply_msg(msg, return_function=True)

    if len(recorder.msg_list) > 0 and recorder.msg_list[-1].content == msg.content and recorder.last_reply != msg.content:
        if str(msg.content).strip() not in ("", " ", "[图片]", "[表情]"):
            logger.info("RUNTIMELOG " + str(msg.group_code) + " repeating, trying to reply " + str(msg.content))
            reply(msg.content)
            recorder.last_reply = msg.content
    recorder.msg_list.append(msg)


@on_group_message(name='basic[三个问题]')
def nick_call(msg, bot):
    if "我是谁" == msg.content:
        bot.reply_msg(msg, "你是{}({})!".format(msg.src_sender_card or msg.src_sender_name, msg.src_sender_id))

    elif "我在哪" == msg.content:
        bot.reply_msg(msg, "你在{name}({id})!".format(name=msg.src_group_name, id=msg.src_group_id))

    elif msg.content in ("我在干什么", "我在做什么"):
        bot.reply_msg(msg, "你在调戏我!!")


@on_discuss_message(name='basic[讨论组三个问题]')
def discuss_three_questions(msg, bot):
    if "我是谁" == msg.content:
        bot.reply_msg(msg, "你是{}!".format(msg.src_sender_name))

    elif "我在哪" == msg.content:
        bot.reply_msg(msg, "你在{name}!".format(name=msg.src_discuss_name))

    elif msg.content in ("我在干什么", "我在做什么"):
        bot.reply_msg(msg, "你在调戏我!!")

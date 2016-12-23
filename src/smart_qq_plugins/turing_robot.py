# coding: utf-8
from random import randint
import requests
import json

from smart_qq_bot.signals import (
        on_all_message,
        on_group_message
        )

# 使用前请先前往 http://www.tuling123.com/register/index.jhtml
# 申请 API key 谢谢
# 另外需要 requests 支持
# 修改成调用图灵官方接口
always_on = {}
url = 'http://www.tuling123.com/openapi/api'
apikey = '555f72fcc51a468c88614e9f3d1beb66'

@on_group_message(name='turing_robot')
def turing_robot(msg, bot):
    """
    :type bot: smart_qq_bot.bot.QQBot
    :type msg: smart_qq_bot.messages.QMessage
    """

    global always_on
    if msg.group_id not in always_on:
        always_on[msg.group_id] = False
    querystring = {
        "key": apikey,
        "info": msg.content,
    }

    if 'Elisa' in msg.content or always_on[msg.group_id]:
        querystring['info'] = querystring['info'].replace('Elisa', '')
        response = requests.request("GET", url, params=querystring)

        response_json = response.json()
        reply_m = ''
        for data in response_json.values():
            if isinstance(data, str):
                reply_m += data + '\n'
            elif isinstance(data, list):
                for i, _data in enumerate(data):
                    if i == 4:
                        break
                    try:
                        _data.pop('icon')
                    except KeyError:
                        pass
                    for __data in _data.values():
                        reply_m += __data + '\n'

        bot.reply_msg(msg, reply_m)
    elif msg.content == '!always_turing':
        always_on[msg.group_id] = True
    elif msg.content == '!noalways_turing':
        always_on[msg.group_id] = False

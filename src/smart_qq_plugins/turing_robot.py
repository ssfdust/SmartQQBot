# coding: utf-8
from random import randint
import requests
import json
import re

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
reg = re.compile(r'(Elisa|@Elisa)')

@on_group_message(name='turing_robot')
def turing_robot(msg, bot):
    """
    :type bot: smart_qq_bot.bot.QQBot
    :type msg: smart_qq_bot.messages.QMessage
    """

    global always_on
    if msg.group_code not in always_on:
        always_on[msg.group_code] = False
    group_code = str(msg.group_code)
    group_id = str(bot.get_group_info(group_code=group_code).get('id'))

    querystring = {
        "key": apikey,
        "info": msg.content,
        "userid": group_id
    }
    if msg.content == '!always_turing':
        always_on[msg.group_code] = True
    elif msg.content == '!noalways_turing':
        always_on[msg.group_code] = False
    elif 'Elisa' in msg.content or always_on[msg.group_code]:
        querystring['info'] = re.sub(reg, '', querystring['info'])
        if '成语接龙' in querystring['info']:
            always_on[msg.group_code] = True
        if re.match(' 帮助$', querystring['info']) or re.match('^[\s]*翻译\s',  querystring['info']):
            return False
        response = requests.request("POST", url, params=querystring)

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
        
        reply_m = re.sub(r'\n$', '', reply_m)
        if '你接错了，退出成语接龙模式' in reply_m:
            always_on[msg.group_code] = False
        bot.reply_msg(msg, reply_m)


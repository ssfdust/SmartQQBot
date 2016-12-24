# -*- coding: utf-8 -*-

import re
import subprocess
from smart_qq_bot.signals import on_all_message

@on_all_message
def translate(msg, bot):
    string = ''
    if "翻译" in msg.content:
        tmp_str = str(msg.content)
        target_str = tmp_str.replace('翻译', '')
        reg_ex = re.match(r'([a-zA-Z- ]*)', target_str)
        if reg_ex.string == reg_ex.group(0):
            res = subprocess.Popen('ydcv' + reg_ex.group(0),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
            result = res.stdout.readlines()

            for sentence in result:
                string += sentence.decode('utf8')

            bot.reply_msg(msg, string)

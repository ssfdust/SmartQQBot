# -*- coding: utf-8 -*-

import re
import os
import subprocess
import requests
import json
from smart_qq_bot.signals import on_all_message
from smart_qq_bot.logger import logger

@on_all_message
def translate(msg, bot):
    path = os.getcwd()
    string = ''
    if re.search('\s*翻译 ',msg.content):
        tmp_str = str(msg.content)
        target_str = tmp_str.replace('翻译', '')
        target_str = re.sub('(Elisa|@Elisa)', '', target_str)
        if len(target_str.split(' ')) < 4 and not whether_ch_long(target_str):
            res = subprocess.Popen('ydcv' + target_str,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
            result = res.stdout.readlines()

            for sentence in result:
                string += sentence.decode('utf8')
            string += "Powered by ydcv"
        else:
            if contain_chinese(target_str):
                string = google_translate('en', target_str)
                logger.info("Translating {} to English".format(target_str))
            else:
                string = google_translate('zh-CN', target_str)
                logger.info("Translating {} to Chinese".format(target_str))

            string += "\nPowered by Google Translation"

        bot.reply_msg(msg, string)

def whether_ch_long(string):
    for ch in string:
        if u'\u4e00' <= ch <= '\u9fff':
            if len(string) > 5:
                return True
    return False

def contain_chinese(string):
    for ch in string:
        if u'\u4e00' <= ch <= '\u9fff':
            return True
    return False

def google_translate(to_l, text):
    fr_l = google_detect(text)
    url = 'https://translation.googleapis.com/language/translate/v2?'
    params = {'key':'AIzaSyCF9-tN_jND33ZqQ697Tfhg0pUTxQ9Bzgw', 'q': text, 'source':fr_l, 'target':to_l, 'format':'text'}
    trans_r = requests.get(url, params=params)
    data = json.loads(trans_r.text)
    if 'error' in data:
        logger.info('Google transalte error')
        return '翻译出错'

    for i in data['data']['translations']:
        return i['translatedText']

def google_detect(text):
    detect_url = 'https://translation.googleapis.com/language/translate/v2/detect?'
    params =  {'key':'AIzaSyCF9-tN_jND33ZqQ697Tfhg0pUTxQ9Bzgw', 'q':text}
    detect_r = requests.get(detect_url, params=params)
    data = json.loads(detect_r.text)
    return data['data']['detections'][0][0]['language']

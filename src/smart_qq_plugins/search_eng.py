import re
import requests

from html.parser import HTMLParser
from smart_qq_bot.signals import on_all_message
from smart_qq_bot.logger import logger

cmd_google = re.compile(r"google\{(.*?)\}([{a-z}]*)$")
cmd_wiki = re.compile(r"wiki\{(.*?)\}")
cmd_moewiki = re.compile(r"moewiki\{(.*?)\}$")
cmd_archwiki = re.compile(r"archwiki\{(.*?)\}$")

class google_parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = list()
        self.site_processing = False
        self.title_processing = False
        self.des_processing = False
        self.date_processing = False
        self.tmp_dict = dict()
        self.tmp_title = ''
        self.tmp_site = ''
        self.tmp_des = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'cite':
            for key, value in attrs:
                if key == 'class' and value == '_Rm':
                    self.site_processing = True
        if tag == 'h3':
            for key, value in attrs:
                if key == 'class' and value == 'r':
                    self.title_processing = True
        if tag == 'span':
            for key, value in attrs:
                if key == 'class' and value == 'st':
                    self.des_processing = True
                elif key == 'class' and value == 'f':
                    self.date_processing = True

    def handle_data(self, data):
        if self.site_processing == True:
            self.tmp_site += data
        if self.title_processing == True:
            self.tmp_title += data
        if self.des_processing == True:
            self.tmp_des += data 

    def handle_endtag(self, tag):
        if self.site_processing == True and tag == 'cite':
            self.tmp_dict['site'] = self.tmp_site
            self.tmp_site = ''
            self.site_processing = False
        if self.title_processing == True and tag == 'h3':
            self.tmp_dict['title'] = self.tmp_title
            self.tmp_title = ''
            self.title_processing = False
        if self.des_processing == True and tag == 'span':
            if self.date_processing == True:
                self.date_processing = False
                return 1
            self.tmp_dict['des'] = self.tmp_des
            self.tmp_des = ''
            self.des_processing = False
            self.result.append(self.tmp_dict)
            self.tmp_dict = dict()

class arch_parser(HTMLParser):

    """Docstring for arch_parser. """

    def __init__(self):
        HTMLParser.__init__(self)
        self.text = ''
        self.div_processing = False
        self.key = ''
        self.p_pre_processing = False
        self.processing = False
        self.title_processing = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for key, value in attrs: 
                if key == 'id' and value == 'mw-content-text':
                    self.div_processing = True
        elif tag == 'p' and self.div_processing == True:
            self.p_pre_processing = True
        elif tag == 'h1':
            for key, value in attrs:
                if key == 'id' and value == 'firstHeading':
                    self.title_processing = True

    def handle_data(self, data):
        if self.processing == True:
            self.text += data
            return 0
        elif self.p_pre_processing:
            if self.key in data:
                self.processing = True
                self.text += data
        elif self.title_processing == True:
            self.key = data 

    def handle_endtag(self, tag):
        if tag == 'p' and self.processing == True:
            self.div_processing = False
            self.p_pre_processing = False
            self.processing = False
        elif tag == 'h1' and self.title_processing == True:
            self.title_processing = False

@on_all_message(name='search_engine[]')
def search_engine(msg, bot):
    ret = ''
    reply = bot.reply_msg(msg, return_function=True)
    google_match = re.match(cmd_google, msg.content)
    archwiki_match = re.match(cmd_archwiki, msg.content)
    if google_match:
        key = google_match.group(1)
        logger.info("Now search for the {} on Google".format(key))
        ret = google_search(key)
        part = ''
        for item in ret:
            part = item['title'] + '\n' + item['site'] + '\n' + item['des']
            reply(part)
    elif archwiki_match:
        key = archwiki_match.group(1)
        logger.info("Now search for the {} on arch wiki".format(key))
        ret = arch_wiki_search(key)
        reply(ret)

def arch_wiki_search(key):
    url_head = 'https://wiki.archlinux.org/index.php/'
    result = ''
    search_head = 'https://wiki.archlinux.org/index.php/Special:Search/'
    ret = requests.get(search_head + key)
    if search_head in ret.url:
        result = '页面不存在'
    else:
        arch_p = arch_parser()
        arch_p.feed(ret.text)
        print(arch_p.key)
        text = str(arch_p.text).split('\n')
        result += str(ret.url).replace(url_head, '') + '\n'
        result += text[-2] + '\n'
        result += ret.url

    return result

def google_search(key):
    url = 'https://www.google.com.hk/search'
    payload = {'nl':'en', 'q': key, 'start':0, 'num':4}
    headers = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    google_r = requests.get(url, params=payload, headers=headers)
    google_r.encoding = 'utf8'
    google_p = google_parser()
    google_p.feed(google_r.text)

    return google_p.result


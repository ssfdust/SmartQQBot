#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Code by Yinzo:        https://github.com/Yinzo
# Origin repository:    https://github.com/Yinzo/SmartQQBot
import logging
import socket

import sys
from smart_qq_bot.config import init_logging

from smart_qq_bot.msg_handler import MsgHandler
from smart_qq_bot.login import QQ


def patch():
    reload(sys)
    sys.setdefaultencoding("utf-8")


def run():
    patch()
    init_logging(logging.DEBUG)
    bot = QQ()
    bot.login()
    bot_handler = MsgHandler(bot)
    while 1:
        try:
            new_msg = bot.check_msg()
            if new_msg is not None:
                bot_handler.handle(new_msg)
        except socket.timeout as e:
            logging.warning("RUNTIMELOG check msg timeout, retrying...")
            continue
        except Exception:
            continue

if __name__ == "__main__":
    run()


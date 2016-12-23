import re
from smart_qq_bot.signals import on_all_message

cmd_google = re.compile(r"!google\{(.*?)\}")
cmd_wiki = re.compile(r"!wiki\{(.*?\}")
cmd_moewiki = re.compile(r"!moewiki\{.*?\}")


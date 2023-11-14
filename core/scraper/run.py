from bot.bot import Bot
import os
import json

obj = Bot()
obj.start_request("https://www.indeed.com/")
obj.search("software engineer")
obj.get_jobs()

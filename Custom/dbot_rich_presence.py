from pypresence import Presence
import time
from threading import Thread
from discord.ext import commands
from asyncio import new_event_loop, set_event_loop


def start_rich_presence():
    loop = new_event_loop()
    set_event_loop(loop)

    client_id = "1023113143486005319"
    RPC = Presence(client_id)

    RPC.connect()
    RPC.update(details='DBot - Discord Selfbot',
               state='Удобный, многофункциональный.',
               start=time.time(),
               large_image='icon',
               large_text='DBot Icon',
               buttons=[{
                   'label': 'Скачать DBot',
                   'url': 'https://github.com/Its-MatriX/DBot-Selfbot'
               }, {
                   'label': 'Сервер',
                   'url': 'https://discord.gg/EC4tDfQYwf'
               }])

    while True:
        time.sleep(15)


class RichPresenceCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        Thread(target=start_rich_presence).start()


def setup(bot):
    bot.add_cog(RichPresenceCog(bot))

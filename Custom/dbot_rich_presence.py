# Для примера, Rich Presence для Discord. Можете удалить, или можете не удалять, если хотите поддержать нас.

from discord.ext import commands
from threading import Thread
import DiscordRPC


def rich_presence():
    rpc = DiscordRPC.RPC.Set_ID(
        app_id=1023113143486005319)  # Connecting to DBot application

    rpc.set_activity(state="Powerful discord selfbot.",
                     details="DBot - Selfbot",
                     large_image='icon',
                     buttons=DiscordRPC.button(
                         'Скачать', 'Наш сервер',
                         'https://github.com/Its-MatriX/DBot-Selfbot',
                         'https://discord.gg/EC4tDfQYwf'))

    rpc.run()


class RichPresenceCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        Thread(target=rich_presence).start()


def setup(bot):
    bot.add_cog(RichPresenceCog(bot))

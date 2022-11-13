from discord.ext import commands
from random import choice, randint, seed
from requests import get
from Functions.logger import log_error
from discord import User


class NSFWCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='porn')
    async def porn__(self, ctx, ptype=None):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not ctx.channel.nsfw:
            log_error('Команда "porn" отправлена в канал без метки NSFW.')
            return

        if not ptype:
            ptype = choice([
                'cosplay', 'hental', 'ass', 'pgif', 'swimsult', 'thigh',
                'hass', 'boobs', 'hboobs', 'pussy', 'anal', 'blowjob',
                'tentacle'
            ])

        path = 'https://nekobot.xyz/api/image?type=' + ptype

        response = get(path)

        if response.ok:
            await ctx.send(response.json()['message'])

        else:
            log_error(f'{response.status_code} {response.json()["message"]}')


def setup(bot):
    bot.add_cog(NSFWCog(bot))

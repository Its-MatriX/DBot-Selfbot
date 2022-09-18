from colorama import Fore
from discord.ext import commands


class CheckerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='check')
    async def check__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.add_reaction('✅')


def setup(bot):
    bot.add_cog(CheckerCog(bot))

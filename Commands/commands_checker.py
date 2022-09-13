from discord.ext import commands
from colorama import Fore


class CheckerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='check')
    async def check__(self, ctx):
        if ctx.author != self.bot.user:
            return

        if self.bot.show_logs:
            print(Fore.GREEN + 'Проверка селфбота: ' + Fore.CYAN +
                  f'Селфбот работает')

        await ctx.message.add_reaction('✅')


def setup(bot):
    bot.add_cog(CheckerCog(bot))
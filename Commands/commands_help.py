from discord.ext import commands
from webbrowser import open_new_tab


class HelpCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help__(self, ctx, command=None):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not command:
            open_new_tab('https://its-matrix.gitbook.io/dbot/')

        else:
            command = command.lower()

            if command in ('fun', 'фан', 'веселье', 'развлечения'):
                open_new_tab('https://its-matrix.gitbook.io/dbot/commands/fun')

            elif command in ('tools', 'инструменты'):
                open_new_tab(
                    'https://its-matrix.gitbook.io/dbot/commands/tools')

            elif command in ('mod', 'мод', 'moderation', 'модерация'):
                open_new_tab(
                    'https://its-matrix.gitbook.io/dbot/commands/moderation')

            elif command in ('info', 'инфо', 'information', 'информация'):
                open_new_tab(
                    'https://its-matrix.gitbook.io/dbot/commands/info')

            elif command in ('random', 'random-api', 'рандом', 'рандом-апи',
                             'случайный-апи', 'случайный'):
                open_new_tab(
                    'https://its-matrix.gitbook.io/dbot/commands/some-random-api'
                )

            elif command in ('nuke', 'краш'):
                open_new_tab(
                    'https://its-matrix.gitbook.io/dbot/commands/nuke')

            elif command in ('auto', 'авто', 'автоответчик', 'авто-ответчик',
                             'авто-ответ', 'auto-response'):
                open_new_tab(
                    'https://its-matrix.gitbook.io/dbot/commands/auto-bot')

            elif command in ('animation', 'anim', 'анимация', 'аним'):
                open_new_tab(
                    'https://its-matrix.gitbook.io/dbot/commands/animation')

            elif command in ('copy', 'копирование', 'скопировать'):
                open_new_tab(
                    'https://its-matrix.gitbook.io/dbot/commands/copy')
                
            elif command in ('nsfw', 'porn', 'порн', 'порно', 'нсфв'):
                open_new_tab(
                    'https://its-matrix.gitbook.io/dbot/commands/nsfw')

            else:
                await ctx.send(f'> **❌ Категории `{command}` не существует. ' + \
                               f'Введите `{self.bot.command_prefix}help` для открытия страницы DBot.**')


def setup(bot):
    bot.add_cog(HelpCog(bot))

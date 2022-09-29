from discord.ext import commands
from discord import User
from urllib.parse import quote
from re import sub


class RandomAPICog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ytcomment')
    async def ytcomment__(self, ctx, user: User, *, comment):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        username = user.display_name

        if len(username) > 25:
            username = username[:21] + '...'

        username = quote(user.display_name)

        username = sub('(\%20)+', '%20', username)

        resp = 'https://some-random-api.ml/canvas/youtube-comment' + '?username=' + username + '&avatar=' + str(
            user.avatar_url_as(format='png')) + '&comment=' + quote(comment)

        await ctx.send(resp)

    @commands.command(name='tweet')
    async def tweet__(self, ctx, user: User, *, comment):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        username = user.name

        if len(username) > 25:
            username = username[:21] + '...'

        username = quote(username)

        username = sub('(\%20)+', '%20', username)

        display_name = user.display_name

        if len(display_name) > 25:
            display_name = display_name[:21] + '...'

        display_name = quote(display_name)

        display_name = sub('(\%20)+', '%20', display_name)

        resp = 'https://some-random-api.ml/canvas/tweet' + '?username=' + username + '&displayname=' + display_name + '&avatar=' + str(
            user.avatar_url_as(format='png')) + '&comment=' + quote(comment)

        await ctx.send(resp)

    @commands.command(name='pixelate')
    async def pixelate__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/pixelate' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='blur')
    async def blur__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/blur' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='stupid')
    async def stupid__(self, ctx, user: User, *, say):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/its-so-stupid' + '?avatar=' + str(
            user.avatar_url_as(format='png')) + '&dog=' + quote(say)

        await ctx.send(resp)

    @commands.command(name='simpcard')
    async def simpcard__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/simpcard' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='horny')
    async def horny__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/horny' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='lolice')
    async def lolice__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/lolice' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='lgbt')
    async def lgbt__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/lgbt' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='pansexual')
    async def pansexual__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/pansexual' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='nonbinary')
    async def nonbinary__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/nonbinary' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='lesbian')
    async def lesbian__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/lesbian' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='bi')
    async def bi__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/bisexual' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='trans')
    async def trans__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/transgender' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='gay')
    async def gay__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/gay' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='glass')
    async def glass__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/glass' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='wasted')
    async def wasted__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/wasted' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='passed')
    async def passed__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/passed' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='jail')
    async def jail__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/jail' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='communist')
    async def communist__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/comrade' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)

    @commands.command(name='triggered')
    async def triggered(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'https://some-random-api.ml/canvas/triggered' + '?avatar=' + str(
            user.avatar_url_as(format='png'))

        await ctx.send(resp)


def setup(bot):
    bot.add_cog(RandomAPICog(bot))

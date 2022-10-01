from os import remove
from os.path import sep, split
from re import sub

from discord import CustomActivity, Member, Status, User
from discord.ext import commands

folder = split(__file__)[0]
datafolder = split(folder)[0] + sep + 'Data'

class CopyCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='copy_avatar')
    async def copy_avatar__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        extension = str(user.avatar_url).split('.')[-1]
        path = sub(r'\?size\=\d+', '',
                   datafolder + sep + 'user_avatar.' + extension)

        await user.avatar_url.save(path)

        avatar = open(path, 'rb')
        avatar_bytes = avatar.read()
        avatar.close()

        await self.bot.user.edit(avatar=avatar_bytes)

        remove(path)

    @commands.command(name='copy_status')
    async def copy_status__(self, ctx, user: Member):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        user_activity = None

        for activity in user.activities:
            if isinstance(activity, CustomActivity):
                user_activity = activity

        if user.status != Status.offline:
            status = user.status
        else:
            status = None

        if status and user_activity:
            await self.bot.change_presence(activity=user_activity,
                                           status=status)

    @commands.command(name='copy_guild_nick')
    async def copy_guild_nick__(self, ctx, user: Member):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        await ctx.author.edit(nick=user.display_name)

    @commands.command(name='copy_all')
    async def copy_all__(self, ctx, user: Member):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        await ctx.author.edit(nick=user.display_name)

        user_activity = None

        for activity in user.activities:
            if isinstance(activity, CustomActivity):
                user_activity = activity

        if user.status != Status.offline:
            status = user.status
        else:
            status = None

        if status and user_activity:
            await self.bot.change_presence(activity=user_activity,
                                           status=status)

        extension = str(user.avatar_url).split('.')[-1]
        path = sub(r'\?size\=\d+', '',
                   datafolder + sep + 'user_avatar.' + extension)

        await user.avatar_url.save(path)

        avatar = open(path, 'rb')
        avatar_bytes = avatar.read()
        avatar.close()

        await self.bot.user.edit(avatar=avatar_bytes)

        remove(path)


def setup(bot):
    bot.add_cog(CopyCog(bot))

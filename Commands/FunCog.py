from discord.ext import commands

ReactionTroll = {
    'enabled': False,
    'guildID': None,
    'userID': None,
    'reaction': None
}

RepeatTroll = {
    'enabled': False,
    'guildID': None,
    'userID': None
}

MessageDeleteTroll = {
    'enabled': False,
    'guildID': None,
    'userID': None
}


class funCog(commands.Cog):

    reactions_command_is_working = False

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reaction_troll')
    async def reaction_troll__(self, ctx, user, react):
        if ctx.author != self.bot.user:
            return

        user = user.replace('<@', '')
        user = user.replace('!', '')
        user = user.replace('>', '')
        user = int(user)
        user = await self.bot.fetch_user(
            user) if not ctx.guild else await ctx.guild.fetch_member(user)

        ReactionTroll['enabled'] = True
        try:
            ReactionTroll['guildID'] = ctx.guild.id
        except:
            ReactionTroll['guildID'] = 0
        ReactionTroll['userID'] = int(user.id)
        ReactionTroll['reaction'] = react

        await ctx.message.delete()

    @commands.command(name='repeat_troll')
    async def repeat_troll__(self, ctx, user):
        if ctx.author != self.bot.user:
            return

        user = user.replace('<@', '')
        user = user.replace('!', '')
        user = user.replace('>', '')
        user = int(user)
        user = await self.bot.fetch_user(
            user) if not ctx.guild else await ctx.guild.fetch_member(user)

        RepeatTroll['enabled'] = True
        try:
            RepeatTroll['guildID'] = ctx.guild.id
        except:
            ReactionTroll['guildID'] = 0
        RepeatTroll['userID'] = int(user.id)

        await ctx.message.delete()

    @commands.command(name='delete_troll')
    async def delete_troll__(self, ctx, user):
        if ctx.author != self.bot.user:
            return

        user = user.replace('<@', '')
        user = user.replace('!', '')
        user = user.replace('>', '')
        user = int(user)
        user = await self.bot.fetch_user(
            user) if not ctx.guild else await ctx.guild.fetch_member(user)

        MessageDeleteTroll['enabled'] = True
        try:
            MessageDeleteTroll['guildID'] = ctx.guild.id
        except:
            MessageDeleteTroll['guildID'] = 0
        MessageDeleteTroll['userID'] = int(user.id)

        await ctx.message.delete()

    @commands.command(name='untroll')
    async def untroll__(self, ctx):
        if ctx.author != self.bot.user:
            return

        ReactionTroll['enabled'] = False
        RepeatTroll['enabled'] = False
        await ctx.message.delete()

    @commands.command(name='reactions')
    async def reactions__(self, ctx, limit, reaction):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        self.reactions_command_is_working = not self.reactions_command_is_working

        if not self.reactions_command_is_working:
            return

        try:
            limit = int(limit)
        except:
            return

        if limit > 10000:
            return

        history = await ctx.channel.history(limit=limit).flatten()

        for message in history:
            if not self.reactions_command_is_working:
                return
            await message.add_reaction(reaction)
        
        self.reactions_command_is_working = False


def setup(bot):
    bot.add_cog(funCog(bot))
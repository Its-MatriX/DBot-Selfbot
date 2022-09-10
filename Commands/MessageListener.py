from discord.ext import commands

from Commands.FunCog import ReactionTroll, RepeatTroll, MessageDeleteTroll


class messageListenerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if ReactionTroll['enabled']:
                try:
                    if message.guild.id == ReactionTroll[
                            'guildID'] or ReactionTroll['guildID'] == 0:
                        if message.author.id == ReactionTroll['userID']:
                            for Reaction in ReactionTroll['reaction']:
                                await message.add_reaction(Reaction)
                except:
                    if message.author.id == ReactionTroll['userID']:
                        for Reaction in ReactionTroll['reaction']:
                            await message.add_reaction(Reaction)
        except:
            pass

        try:
            if RepeatTroll['enabled']:
                try:
                    if message.guild.id == RepeatTroll[
                            'guildID'] or RepeatTroll['guildID'] == 0:
                        if message.author.id == RepeatTroll['userID']:
                            await message.reply(message.content,
                                                mention_author=False)
                except:
                    if message.author.id == RepeatTroll['userID']:
                        await message.reply(message.content,
                                            mention_author=False)
        except:
            pass

        try:
            if MessageDeleteTroll['enabled']:
                try:
                    if message.guild.id == MessageDeleteTroll[
                            'guildID'] or MessageDeleteTroll['guildID'] == 0:
                        if message.author.id == MessageDeleteTroll['userID']:
                            await message.delete()
                except:
                    if message.author.id == MessageDeleteTroll['userID']:
                        await message.delete()
        except:
            pass


def setup(bot):
    bot.add_cog(messageListenerCog(bot))
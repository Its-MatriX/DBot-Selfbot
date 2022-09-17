from asyncio import sleep
from random import choice, uniform

from colorama import Fore
from discord import User
from discord.ext import commands

magicball = [
    "Да",
    "Нет",
    "Возможно",
    "Скорее всего, да",
    "Скорее всего, нет",
    "Конечно",
    "Точно нет",
    "Попробуй спросить позже",
    "Зачем ты меня спрашиваешь?",
    "Можешь быть уверен в этом.",
    "Не уверен...",
    "Знаки говорят - да!",
    "Знаки говорят - нет.",
    "По моим данным - да.",
    "По моим данным - нет."
]

ReactionTroll = {
    'enabled': False,
    'guildID': None,
    'userID': None,
    'reaction': None
}

RepeatTroll = {'enabled': False, 'guildID': None, 'userID': None}

MessageDeleteTroll = {'enabled': False, 'guildID': None, 'userID': None}


def delete_dublicates(source):
    resp = ''
    last = ''

    for letter in source:
        if letter != last:
            resp += letter
        last = letter

    return resp


class FunCog(commands.Cog):

    reactions_command_is_working = False

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reaction_troll')
    async def reaction_troll__(self, ctx, user: User, react):
        if ctx.author != self.bot.user:
            return

        if ctx.guild:
            user_ = ctx.guild.get_member(user.id)
            if user_:
                user = user_

        ReactionTroll['enabled'] = True
        try:
            ReactionTroll['guildID'] = ctx.guild.id
        except:
            ReactionTroll['guildID'] = 0
        ReactionTroll['userID'] = int(user.id)
        ReactionTroll['reaction'] = react

        await ctx.message.delete()

    @commands.command(name='repeat_troll')
    async def repeat_troll__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        if ctx.guild:
            user_ = ctx.guild.get_member(user.id)
            if user_:
                user = user_

        RepeatTroll['enabled'] = True
        try:
            RepeatTroll['guildID'] = ctx.guild.id
        except:
            ReactionTroll['guildID'] = 0
        RepeatTroll['userID'] = int(user.id)

        await ctx.message.delete()

    @commands.command(name='delete_troll')
    async def delete_troll__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        if ctx.guild:
            user_ = ctx.guild.get_member(user.id)
            if user_:
                user = user_

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
        MessageDeleteTroll['enabled'] = False

        await ctx.message.delete()

    @commands.command(name='reactions')
    async def reactions__(self, ctx, limit=None, reaction=None):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not limit and not reaction:
            self.reactions_command_is_working = False

        else:
            self.reactions_command_is_working = True

        if not self.reactions_command_is_working:
            return

        try:
            limit = int(limit)
        except:
            return

        if limit > 10000:
            return

        message_number = 1

        history = await ctx.channel.history(limit=limit).flatten()

        messages_amount = len(history)

        for message in history:
            if not self.reactions_command_is_working:
                return
            await message.add_reaction(reaction)

            message_number += 1

        self.reactions_command_is_working = False

    @commands.command(name='ball')
    async def ball__(self, ctx, *, question):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        selected = choice(magicball)
        resp = f'**{question}**\n:crystal_ball: `Шар думает...`'

        message = await ctx.send(resp)

        await sleep(uniform(1.5, 3))

        resp = f'**{question}**\n:crystal_ball: `{selected}`'

        await message.edit(content=resp)

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.guild:
                if message.author.id == ReactionTroll['userID']:
                    if message.guild.id == ReactionTroll['guildID']:
                        if ReactionTroll['enabled']:
                            try:
                                selected = choice(ReactionTroll['reaction'])
                                await message.add_reaction(selected)
                            except Exception as e:

                                if 'unknown message' in e.args.lower():
                                    return

                                ReactionTroll['reaction'] = ReactionTroll['reaction'].replace(
                                    selected, '')
                                selected = choice(ReactionTroll['reaction'])
                                await message.add_reaction(selected)

            else:
                if message.author.id == ReactionTroll['userID']:
                    if ReactionTroll['enabled']:
                        try:
                            selected = choice(ReactionTroll['reaction'])
                            await message.add_reaction(selected)
                        except:
                            ReactionTroll['reaction'] = ReactionTroll['reaction'].replace(
                                selected, '')
                            selected = choice(ReactionTroll['reaction'])
                            await message.add_reaction(selected)

            if message.guild:
                if message.author.id == RepeatTroll['userID']:
                    if message.guild.id == RepeatTroll['guildID']:
                        if RepeatTroll['enabled']:
                            await message.channel.send(message.content)

            else:
                if message.author.id == RepeatTroll['userID']:
                    if RepeatTroll['enabled']:
                        await message.channel.send(message.content)

            if message.guild:
                if message.author.id == MessageDeleteTroll['userID']:
                    if message.guild.id == MessageDeleteTroll['guildID']:
                        if MessageDeleteTroll['enabled']:
                            await message.delete()

            else:
                pass

        except Exception as e:
            try:
                if 'unknown message' in e.args.lower():
                    return
            except:
                pass


def setup(bot):
    bot.add_cog(FunCog(bot))

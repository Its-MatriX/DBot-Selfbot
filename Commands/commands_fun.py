from asyncio import sleep
from random import choice, randint, uniform

from discord import User
from discord.ext import commands

magicball = [
    "Да", "Нет", "Возможно", "Скорее всего, да", "Скорее всего, нет",
    "Конечно", "Точно нет", "Попробуй спросить позже",
    "Зачем ты меня спрашиваешь?", "Можешь быть уверен в этом.", "Не уверен...",
    "Знаки говорят - да!", "Знаки говорят - нет.", "По моим данным - да.",
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
    pings_is_working = False

    def __init__(self, bot):
        self.bot = bot

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

                                ReactionTroll['reaction'] = ReactionTroll[
                                    'reaction'].replace(selected, '')
                                selected = choice(ReactionTroll['reaction'])
                                await message.add_reaction(selected)

            else:
                if message.author.id == ReactionTroll['userID']:
                    if ReactionTroll['enabled']:
                        try:
                            selected = choice(ReactionTroll['reaction'])
                            await message.add_reaction(selected)
                        except:
                            ReactionTroll['reaction'] = ReactionTroll[
                                'reaction'].replace(selected, '')
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

    @commands.command(name='textmoji')
    async def textmoji__(self, ctx, *, text):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        text = text.lower()
        text = text.replace(' ', '    ').replace('10', '🔟').replace(
            'ab',
            '\u200B🆎').replace('cl', '\u200B🆑').replace('0', '0️⃣').replace(
                '1', '1️⃣').replace('2', '2️⃣').replace('3', '3️⃣').replace(
                    '4',
                    '4️⃣').replace('5', '5️⃣').replace('6', '6️⃣').replace(
                        '7',
                        '7️⃣').replace('8', '8️⃣').replace('9', '9️⃣').replace(
                            '!', '\u200B❗').replace('?', '\u200B❓').replace(
                                'vs',
                                '\u200B🆚').replace('.', '\u200B🔸').replace(
                                    ',', '🔻').replace('a', '\u200B🅰').replace(
                                        'b', '\u200B🅱'
                                    ).replace('c', '\u200B🇨').replace(
                                        'd', '\u200B🇩').replace(
                                            'e', '\u200B🇪'
                                        ).replace('f', '\u200B🇫').replace(
                                            'g', '\u200B🇬'
                                        ).replace('h', '\u200B🇭').replace(
                                            'i', '\u200B🇮'
                                        ).replace('j', '\u200B🇯').replace(
                                            'k', '\u200B🇰'
                                        ).replace('l', '\u200B🇱').replace(
                                            'm', '\u200B🇲'
                                        ).replace('n', '\u200B🇳').replace(
                                            'ñ', '\u200B🇳'
                                        ).replace('o', '\u200B🅾').replace(
                                            'p', '\u200B🅿'
                                        ).replace('q', '\u200B🇶').replace(
                                            'r', '\u200B🇷'
                                        ).replace('s', '\u200B🇸').replace(
                                            't', '\u200B🇹'
                                        ).replace('u', '\u200B🇺').replace(
                                            'v', '\u200B🇻').replace(
                                                'w', '\u200B🇼').replace(
                                                    'x', '\u200B🇽').replace(
                                                        'y',
                                                        '\u200B🇾').replace(
                                                            'z',
                                                            '\u200B🇿').replace(
                                                                '<',
                                                                '◀️').replace(
                                                                    '>', '▶️')

        await ctx.send(text)

    @commands.command(name='virus')
    async def virus__(self, ctx, virus, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        anim = f'''Preparing...
Fetching download servers...
Fetching download servers... dl-virus.download/{virus}-virus.exe
Fetching download servers... dl-virus.download/{virus}-virus.exe [ERROR]
Fetching download servers... virus-mirror.main/{virus}-virus.exe
Fetching download servers... virus-mirror.main/{virus}-virus.exe [OK]
Selected virus-mirror.main/{virus}-virus.exe
Preparing download...
Connecting to download server...
Successfully connected - virus-mirror.main/{virus}-virus.exe
Downloading - virus-mirror.main/{virus}-virus.exe
[▓▓▓                    ] / {virus}-virus.exe | Packing files.
[▓▓▓▓▓▓▓                ] - {virus}-virus.exe | Packing files..
[▓▓▓▓▓▓▓▓▓▓▓▓           ] \ {virus}-virus.exe | Packing files..
[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] | {virus}-virus.exe | Packing files..
[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ] / {virus}-virus.exe | Packing files..
[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ] - {virus}-virus.exe | Packing files..
[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ] \ {virus}-virus.exe | Packing files..
Successfully downloaded {virus}-virus.exe
Connecting to remote device... |
Connecting to remote device... /
Connecting to remote device... -
Connecting to remote device... Done
[▓▓▓                    ] 3/25 MiB | Moving {virus}-virus.exe to remote device...
[▓▓▓▓▓▓▓                ] 7/25 MiB | Moving {virus}-virus.exe to remote device...
[▓▓▓▓▓▓▓▓▓▓▓▓           ] 13/25 MiB | Moving {virus}-virus.exe to remote device...
[▓▓▓▓▓▓▓▓▓▓▓▓▓▓         ] 16/25 MiB | Moving {virus}-virus.exe to remote device...
[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓      ] 20/25 MiB | Moving {virus}-virus.exe to remote device...
[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ] 23/25 MiB | Moving {virus}-virus.exe to remote device...
[▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ] 25/25 MiB | Moving {virus}-virus.exe to remote device...
Successfully moved {virus}-virus.exe to remote device
Starting {virus}-virus.exe on remote device...
Starting {virus}-virus.exe on remote device... Done
Injecting virus.   |
Injecting virus..  /
Injecting virus... -
Successfully Injected {virus}-virus.exe into {user.display_name}'''.split('\n')

        message = await ctx.send('``' + anim[0] + '``')

        for frame in anim[1:]:
            await message.edit(content='``' + frame + '``')
            await sleep(.5)

    @commands.command(name='pings')
    async def pings__(self, ctx, amount: int = None, user: User = None):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not amount:
            self.pings_is_working = False
            return

        if not user:
            self.pings_is_working = False
            return

        self.pings_is_working = not self.pings_is_working

        if not self.pings_is_working:
            return

        for x in range(amount):

            if not self.pings_is_working:
                return

            await ctx.trigger_typing()
            await sleep(2)
            await ctx.send(user.mention * randint(1, 5))
            await sleep(3)

    @commands.command(name='hehe')
    async def hehe__(self, ctx, length: int = 30):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = ''
        char = choice([True, False])

        for x in range(length):
            char = not char

            if randint(1, 5) != 1:

                if char:
                    resp += 'А'
                else:
                    resp += 'Х'
            else:
                if not char:
                    resp += 'А'
                else:
                    resp += 'Х'

        await ctx.send(resp)

    @commands.command(name='oof')
    async def oof__(self, ctx, length: int = 3):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        case = choice([True, False])

        if length < 3:
            raise TypeError('Длина OOF не может быть меньше 3 символов!')

        length_ooo = length - 1

        resp = ''

        for x in range(length_ooo):
            if case:
                resp += 'O'

            else:
                resp += 'o'

            case = not case

        if case:
            resp += 'F'

        else:
            resp += 'f'

        await ctx.send(resp)

    @commands.command(name='flip')
    async def flip__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        anim = '''`(\°-°)\  ┬─┬
(\°□°)\  ┬─┬
(-°□°)-  ┬─┬
(╯°□°)╯    ]
(╯°□°)╯     ┻━┻
(╯°□°)╯       [
(╯°□°)╯          ┬─┬
(╯°□°)╯                 ]
(╯°□°)╯                  ┻━┻
(╯°□°)╯                         [
(\°-°)\                               ┬─┬
(\°-°)\                                     ]
(\°-°)\                                       ┻━┻
(\°-°)\                                               [
(\°-°)\                                              ┬─┬'''.split('\n')

        message = await ctx.send('``' + anim[0] + '``')

        for frame in anim[1:]:
            await message.edit(content='``' + frame + '``')
            await sleep(.3)

    @commands.command(name='handjob')
    async def handjob__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        anim = [
            '8✊=====D',
            '8=✊====D',
            '8==✊===D',
            '8===✊==D',
            '8====✊=D',
            '8=====✊D',
            '8====✊=D',
            '8===✊==D',
            '8==✊===D',
            '8=✊====D',
            '8✊=====D',
            '8✊=====D',
            '8=✊====D',
            '8==✊===D',
            '8===✊==D',
            '8====✊=D💦',
            '8=====✊D💦',
        ]

        message = await ctx.send(anim[0])

        for frame in anim[1:]:
            await message.edit(content=frame )
            await sleep(.3)

    @commands.command(name='token')
    async def token__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        starts = ['OTgW', 'OTg0', 'OTIw', 'MTAx', 'MTAw', 'OTE3']

        characters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
        part_a = "".join(choice(characters) for x in range(20))
        part_b = "".join(choice(characters) for x in range(6))
        part_c = "".join(choice(characters) for x in range(27))

        resp = choice(starts) + part_a + '.' + part_b + '.' + part_c
        
        resp = f'> **Token Hacker** - fetched token for **{user.name}**\n' + \
            f'> `{resp}`'

        await ctx.send(resp)


def setup(bot):
    bot.add_cog(FunCog(bot))

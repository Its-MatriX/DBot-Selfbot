from asyncio import sleep
from base64 import b64encode
from json import dump, load
from os import remove
from os.path import sep, split
from random import choice, choices, randint, uniform
from string import ascii_letters, digits
from time import time

from discord import File, User, Member
from discord.ext import commands
from Functions.demotivators import Demotivator
from Functions.bool_converter import convert_to_bool
from Functions.logger import log_error
from pyfiglet import figlet_format
from webbrowser import open_new_tab

token_generator_part_length = 10

folder = split(__file__)[0]
datafolder = split(folder)[0] + sep + 'Data'

use_default_trolls = True

try:
    file = open(datafolder + sep + 'troll_config.json', 'r')
    use_default_trolls = False
    troll_config = load(file)

    reaction_troll = troll_config['reactionTroll']
    repeat_troll = troll_config['repeatTroll']
    delete_troll = troll_config['deleteTroll']
    group_rename_troll = troll_config['groupRenameTroll']
except:
    use_default_trolls = True

    file = open(datafolder + sep + 'troll_config.json', 'w')
    file.write('{}')
    file.close()

magicball = [
    "Да", "Нет", "Возможно", "Скорее всего, да", "Скорее всего, нет",
    "Конечно", "Точно нет", "Попробуй спросить позже",
    "Зачем ты меня спрашиваешь?", "Можешь быть уверен в этом.", "Не уверен...",
    "Знаки говорят - да!", "Знаки говорят - нет.", "По моим данным - да.",
    "По моим данным - нет."
]

if use_default_trolls:
    reaction_troll = {
        'enabled': False,
        'guildID': None,
        'userID': None,
        'reaction': None
    }

    repeat_troll = {'enabled': False, 'guildID': None, 'userID': None}

    delete_troll = {'enabled': False, 'guildID': None, 'userID': None}

    group_rename_troll = {'enabled': False, 'groupID': None, 'groupName': None}


def delete_dublicates(source):
    resp = ''
    last = ''

    for letter in source:
        if letter != last:
            resp += letter
        last = letter

    return resp


__cursed_chars = (769, 771, 772, 773, 774, 775, 776, 777, 778, 782, 783, 785,
                  786, 789, 791, 793, 794, 796, 799, 800, 801, 802, 803, 804,
                  805, 807, 808, 810, 812, 816, 817, 818, 819, 820, 821, 822,
                  823, 824, 826, 829, 830, 832, 833, 835, 836, 837, 839, 841,
                  842, 844, 846, 850, 852, 853, 854, 855, 857, 859, 860, 861,
                  864)

__alpha_scary_type = {
    'б': '6',
    'с': 's',
    'з': 'z',
    'ч': '4',
    'и': 'u',
    'п': 'n',
    'в': 'v',
    'т': 't',
    'д': 'd',
    'к': 'k',
    'о': '0'
}


def convert_scary_type(text):
    out = ''

    for char in text:
        out += __alpha_scary_type.get(char) if __alpha_scary_type.get(
            char) else char + ''.join(
                [chr(choice(__cursed_chars)) for x in range(randint(0, 3))])

    return out


class FunCog(commands.Cog):

    reactions_command_is_working = False
    pings_is_working = False
    inftype_is_working = False
    move_troll_is_working = False
    enable_scary_type = False

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.inftype_is_working == True and message.author.id == self.bot.user.id:
            self.inftype_is_working = False

        try:
            if message.guild:
                if message.author.id == reaction_troll['userID']:
                    if message.guild.id == reaction_troll['guildID']:
                        if reaction_troll['enabled']:
                            try:
                                selected = choice(reaction_troll['reaction'])
                                await message.add_reaction(selected)
                            except Exception as e:

                                if 'unknown message' in e.args.lower():
                                    return

                                reaction_troll['reaction'] = reaction_troll[
                                    'reaction'].replace(selected, '')
                                selected = choice(reaction_troll['reaction'])
                                await message.add_reaction(selected)

            else:
                if message.author.id == reaction_troll['userID']:
                    if reaction_troll['enabled']:
                        try:
                            selected = choice(reaction_troll['reaction'])
                            await message.add_reaction(selected)
                        except Exception:
                            reaction_troll['reaction'] = reaction_troll[
                                'reaction'].replace(selected, '')
                            selected = choice(reaction_troll['reaction'])
                            await message.add_reaction(selected)

            if message.guild:
                if message.author.id == repeat_troll['userID']:
                    if message.guild.id == repeat_troll['guildID']:
                        if repeat_troll['enabled']:
                            await message.channel.send(message.content)

            else:
                if message.author.id == repeat_troll['userID']:
                    if repeat_troll['enabled']:
                        await message.channel.send(message.content)

            if message.guild:
                if message.author.id == delete_troll['userID']:
                    if message.guild.id == delete_troll['guildID']:
                        if delete_troll['enabled']:
                            await message.delete()

            else:
                pass

        except Exception as e:
            try:
                if 'unknown message' in e.args.lower():
                    return
            except Exception:
                pass

        if self.enable_scary_type:
            if message.author == self.bot.user:
                if not message.content.startswith(self.bot.command_prefix):
                    await message.edit(
                        content=convert_scary_type(message.content))

    @commands.Cog.listener()
    async def on_private_channel_update(self, before, after):
        if after.id == group_rename_troll['groupID']:
            if after.name != group_rename_troll['groupName']:
                if group_rename_troll['enabled']:
                    await after.edit(name=group_rename_troll['groupName'])

    @commands.command(name='reaction_troll')
    async def reaction_troll__(self, ctx, user: User, react):
        if ctx.author != self.bot.user:
            return

        if ctx.guild:
            user_ = ctx.guild.get_member(user.id)
            if user_:
                user = user_

        reaction_troll['enabled'] = True
        try:
            reaction_troll['guildID'] = ctx.guild.id
        except Exception:
            reaction_troll['guildID'] = 0
        reaction_troll['userID'] = int(user.id)
        reaction_troll['reaction'] = react

        save_config = {
            'reactionTroll': reaction_troll,
            'repeatTroll': repeat_troll,
            'deleteTroll': delete_troll
        }

        file = open(datafolder + sep + 'troll_config.json', 'w')
        dump(save_config, file, indent=4)

        await ctx.message.delete()

    @commands.command(name='repeat_troll')
    async def repeat_troll__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        if ctx.guild:
            user_ = ctx.guild.get_member(user.id)
            if user_:
                user = user_

        repeat_troll['enabled'] = True
        try:
            repeat_troll['guildID'] = ctx.guild.id
        except Exception:
            reaction_troll['guildID'] = 0
        repeat_troll['userID'] = int(user.id)

        save_config = {
            'reactionTroll': reaction_troll,
            'repeatTroll': repeat_troll,
            'deleteTroll': delete_troll,
            'groupRenameTroll': group_rename_troll
        }

        file = open(datafolder + sep + 'troll_config.json', 'w')
        dump(save_config, file, indent=4)

        await ctx.message.delete()

    @commands.command(name='delete_troll')
    async def delete_troll__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        if ctx.guild:
            user_ = ctx.guild.get_member(user.id)
            if user_:
                user = user_

        delete_troll['enabled'] = True
        try:
            delete_troll['guildID'] = ctx.guild.id
        except Exception:
            delete_troll['guildID'] = 0
        delete_troll['userID'] = int(user.id)

        save_config = {
            'reactionTroll': reaction_troll,
            'repeatTroll': repeat_troll,
            'deleteTroll': delete_troll,
            'groupRenameTroll': group_rename_troll
        }

        file = open(datafolder + sep + 'troll_config.json', 'w')
        dump(save_config, file, indent=4)

        await ctx.message.delete()

    @commands.command(name='gr_troll')
    async def gr_troll__(self, ctx, *, group_name: str):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        group_rename_troll['enabled'] = True
        group_rename_troll['groupID'] = ctx.channel.id
        group_rename_troll['groupName'] = group_name

        save_config = {
            'reactionTroll': reaction_troll,
            'repeatTroll': repeat_troll,
            'deleteTroll': delete_troll,
            'groupRenameTroll': group_rename_troll
        }

        file = open(datafolder + sep + 'troll_config.json', 'w')
        dump(save_config, file, indent=4)

    @commands.command(name='move_troll')
    async def move_troll(self, ctx, member: Member, moves: int):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        moved_to = None

        self.move_troll_is_working = True

        try:
            for x in range(moves):
                while True:
                    move_to = choice(ctx.guild.voice_channels)

                    if move_to != moved_to:
                        break

                await member.move_to(move_to)
                moved_to = move_to
        except:
            pass

        self.move_troll_is_working = False

    @commands.command(name='untroll')
    async def untroll__(self, ctx):
        if ctx.author != self.bot.user:
            return

        global repeat_troll
        global delete_troll
        global reaction_troll
        global group_rename_troll

        self.move_troll_is_working = False

        reaction_troll = {
            'enabled': False,
            'guildID': None,
            'userID': None,
            'reaction': None
        }

        repeat_troll = {'enabled': False, 'guildID': None, 'userID': None}

        delete_troll = {'enabled': False, 'guildID': None, 'userID': None}

        group_rename_troll = {
            'enabled': False,
            'groupID': None,
            'groupName': None
        }

        save_config = {
            'reactionTroll': reaction_troll,
            'repeatTroll': repeat_troll,
            'deleteTroll': delete_troll,
            'groupRenameTroll': group_rename_troll
        }

        file = open(datafolder + sep + 'troll_config.json', 'w')
        dump(save_config, file, indent=4)

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
        except Exception:
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

    @commands.command(name='token')
    async def token__(self, ctx, user: User):
        # Интересный факт:
        # Начало токена (до первой точки) будет совпадать с настоящим токеном пользователя.
        # (проверено на 5 аккаунтах!)

        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = f'> **Token Hacker** - fetching token for **{user.name}**\n' + \
            f'> `Fetching token in progress...`'

        message = await ctx.send(resp)

        start = time()
        await sleep(uniform(1, 2.5), 2)

        base64_string = "=="
        id_bytes = str(user.id).encode("ascii")
        base64_bytes = b64encode(id_bytes)
        base64_string = base64_bytes.decode("ascii")

        token = base64_string.replace(
            '=', '') + "." + choice(ascii_letters).upper() + ''.join(
                choice(ascii_letters + digits)
                for _ in range(5)) + "." + ''.join(
                    choice(ascii_letters + digits) for _ in range(27))

        parts = [
            token[x:x + token_generator_part_length]
            for x in range(0, len(token), token_generator_part_length)
        ]
        generated = ''

        for part in parts:
            generated += part
            dot_chars = '.' * (len(token) - len(generated))

            resp = f'> **Token Hacker** - fetching token for **{user.name}**\n' + \
            f'> `{generated}{dot_chars}`'

            await message.edit(content=resp)

            await sleep(uniform(.5, 1))

        await message.delete()

        generate_duration = round(time() - start, 2)

        resp = f'> **Token Hacker** - fetched token for **{user.name}** in **{generate_duration}** sec.\n' + \
            f'> `{token}`'

        await ctx.send(resp)

    @commands.command(name='dem')
    async def dem__(self, ctx, *, data):
        if ctx.author != self.bot.user:
            return

        if len(ctx.message.attachments) == 0:
            return

        attachments = ctx.message.attachments

        await ctx.message.delete()

        attachment = attachments[0]

        if ';' not in data:
            top_text = data
            bottom_text = ''
        else:
            splitten = data.split(';', 1)
            top_text = splitten[0]
            bottom_text = splitten[1]

        dem = Demotivator(top_text, bottom_text)
        dem.create(attachment.url,
                   result_filename=datafolder + sep +
                   'demotivator-generated.png',
                   use_url=True,
                   delete_file=True,
                   font_name=datafolder + sep + 'times.ttf')

        file = File(datafolder + sep + 'demotivator-generated.png')
        await ctx.send(file=file)

        remove(datafolder + sep + 'demotivator-generated.png')

    @commands.command(name='ip')
    async def ip__(self, ctx, user: User):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = '.'.join([str(randint(1, 255)) for x in range(4)])

        resp = f'> **IP Hacker** - hacked IP for **{user.name}**\n' + \
            f'> `{resp}`'

        await ctx.send(resp)

    @commands.command(name='gename')
    async def gename__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()
        first, second = choices(ctx.guild.members, k=2)
        first = first.display_name[len(first.display_name) // 2:]
        second = second.display_name[:len(second.display_name) // 2]
        await ctx.send(second + first)

    @commands.command(name='inftype')
    async def inftype__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        self.inftype_is_working = True

        while self.inftype_is_working:
            await ctx.trigger_typing()
            await sleep(8)

    @commands.command(name='scarytype')
    async def scarytype__(self, ctx, enable: str):
        if ctx.author != self.bot.user:
            return

        enable = convert_to_bool(enable)

        await ctx.message.delete()

        self.enable_scary_type = enable

    @commands.command(name='figlet')
    async def figlet__(self, ctx, font, *, text=None):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if font == 'help' and not text:
            open_new_tab('http://www.figlet.org/examples.html')
            return

        converted = figlet_format(text=text, font=font)
        converted = '```' + (converted.replace('`', '\'')) + '```'

        if len(converted) > 2000:
            log_error('"figlet": слишком длинный вывод')
            return

        await ctx.send(converted)


def setup(bot):
    bot.add_cog(FunCog(bot))
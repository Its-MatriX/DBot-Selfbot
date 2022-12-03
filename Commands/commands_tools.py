from asyncio import sleep
from os.path import sep, split

folder = split(__file__)[0]

import io
import random
from base64 import b64decode, b64encode
from json import dump, load
from os import _exit, name, remove
from os.path import expanduser
from re import findall, sub
from time import time
from time import sleep as non_async_sleep

import requests
from colour import Color
from discord import (Activity, ActivityType, File, Game, GroupChannel, Status,
                     Streaming, Guild)
from discord.ext import commands
from Functions.logger import log, log_error
from PIL import Image
from translate import Translator
from keyboard import is_pressed
from threading import Thread
from os import environ
import platform
from pyperclip import copy
from qrcode import make as make_qrcode
from Functions.discord_requests import send_request
from Functions.bool_converter import convert_to_bool
from Functions.attribute_parser import parse_attributes
from Functions.timestamp_converter import convert_timestamp

allow_run_keyboard_listeners = True

if platform.system() == 'Linux':
    if not 'SUDO_UID' in environ.keys():
        allow_run_keyboard_listeners = False

home = expanduser('~')

folder = split(__file__)[0]
datafolder = split(folder)[0] + sep + 'Data'

try:
    file = open(datafolder + sep + 'auto_response.json', 'r')
    auto_response_messages = load(file)
    file.close()
except:
    open(datafolder + sep + 'auto_response.json', 'w').write('{}')
    auto_response_messages = {}

try:
    file = open(datafolder + sep + 'config_commands.json', 'r')
    config_commands = load(file)
    file.close()

    enable_djm = config_commands['enableDJM']
except:
    open(datafolder + sep + 'auto_response.json', 'w').write('{}')

    baseconfig = {'enableDJM': False}
    file = open(datafolder + sep + 'config_commands.json', 'w')
    dump(baseconfig, file, indent=4)
    file.close()

    config_commands = baseconfig

    enable_djm = config_commands['enableDJM']

case_translate_layout_en_ru = dict(
    zip(
        map(
            ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
            'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
        "йцукенгшщзхъфывапролджэячсмитьбю.ё"
        'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))

case_translate_layout_ru_en = dict(
    zip(
        map(
            ord, "йцукенгшщзхъфывапролджэячсмитьбю.ё"
            'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'),
        "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
        'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'))

letters_ru = 'йцукенгшщзхъфывапролджэячсмитьбю'
letters_en = 'qwertyuiopasdfghjklzxcvbnm'


def detect_case(source):
    contains_ru_letters = 0
    contains_en_letters = 0

    for letter in source:
        if letter in letters_ru:
            contains_ru_letters += 1

        elif letter in letters_en:
            contains_en_letters += 1

        else:
            pass

    if contains_ru_letters > contains_en_letters:
        return 'RU'
    elif contains_en_letters >= contains_ru_letters:
        return 'EN'


def random_chars():
    return ''.join(
        [random.choice('QWERTYUIOPASDFGHJKLZXCVBNM') for x in range(4)])


def spam_string_parse(message):
    if not ('?digit' in message or '?letter' in message or '?prep' in message
            or '?char' in message):
        return message

    for x in range(message.count('?digit')):
        message = message.replace('?digit', str(random.randint(0, 9)), 1)

    for x in range(message.count('?letter')):
        message = message.replace('?letter',
                                  random.choice('QWERTYUIOPASDFGHJKLZXCVBNM'),
                                  1)

    for x in range(message.count('?prep')):
        message = message.replace('?prep', random.choice('.!?'), 1)

    if '?char' in message:
        searches_randchar = findall('\?char \d+,\s*\d+', message)

        for s in searches_randchar:
            vals = s.replace('?char ', '').split(',')
            start = int(vals[0])
            end = int(vals[1])
            if start >= end:
                raise TypeError(
                    'Минимальное число не может быть больше максимального')
            if start < 0 or end < 0:
                raise TypeError(
                    '?char <start> или ?char <end> не может быть меньше 0')
            message = message.replace(s, chr(random.randint(start, end)))

    return message


def grammarfix(text):
    text = list(text)
    text[0] = text[0].upper()

    if text[-1] not in ['.', '!', '?']:
        text.append('.')

    text = ''.join(text)
    text = sub('\.{2,}', '...', text)

    text = list(text)

    lastchar = ''
    index = 0

    for char in text:
        if lastchar in ['.', '!', '?']:
            char = char.upper()
            text[index] = char

        index += 1

        if char != ' ':
            lastchar = char

    return ''.join(text)


class ToolsCog(commands.Cog):

    spammer_is_working = False
    stop_spam_keyboard_listener_is_working = False
    grammar_fix_is_working = False

    def __init__(self, bot):
        self.bot = bot
        self.allow_groups = [x.id for x in self.bot.private_channels]

    def listen_stop_spam(self):
        if not allow_run_keyboard_listeners:
            return

        if self.stop_spam_keyboard_listener_is_working:
            return

        log('Нажмите [Ctrl+Alt+S] для остановки спам-атаки.', 'СПАМ')

        self.stop_spam_keyboard_listener_is_working = True
        is_error = False

        try:
            while self.spammer_is_working:
                non_async_sleep(.1)

                if is_pressed('ctrl+alt+s'):
                    self.spammer_is_working = False
                    self.stop_spam_keyboard_listener_is_working = False

                    if not is_error:
                        log('Спам-атака остановлена.', 'СПАМ')

                    break

        except:
            is_error = True

        self.stop_spam_keyboard_listener_is_working = False

    @commands.Cog.listener()
    async def on_message(self, message):
        content = message.content.lower().replace(' ', '').replace('.', '')
        keys = list(auto_response_messages.keys())

        if content in keys:
            await message.reply(auto_response_messages[content],
                                mention_author=False)

        global enable_djm

        if isinstance(message.channel, GroupChannel):
            if message.channel.id not in self.allow_groups:
                if enable_djm:
                    await message.channel.leave()

        try:
            if message.author == self.bot.user:
                if self.grammar_fix_is_working:
                    if message.content != grammarfix(message.content):
                        await message.edit(content=grammarfix(message.content))

        except:
            pass

    @commands.command(name='logout')
    async def logout__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()
        await ctx.send('> **⏹ Выход из аккаунта**')

        await self.bot.close()
        _exit(0)

    @commands.command(name='status')
    async def status__(self, ctx, *, status=None):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not status:
            resp = '🪄 **status <*параметры*>:** `сменить статус`\n' + \
                '`status idle` - сменить иконку на `неактивен`\n' + \
                '\n' + \
                '**Иконки:**\n' + \
                '🟢 `online` - *в сети*\n' + \
                '🟡 `idle` - *неактивен*\n' + \
                '🔴 `dnd` - *не беспокоить*\n' + \
                '⚪ `invisible` - *невидимка*\n' + \
                '\n' + \
                '**Дополнительно:**\n' + \
                '❌ **delete** - `сбросить статус`\n' + \
                '📽️ **streaming <*ссылка на стрим*> <*имя стрима*>** - `стримит`\n' + \
                '🎮 **game <*иконка статуса*> <*имя игры*>** - `играет в`\n' + \
                '📺 **watch <*иконка статуса*> <*имя*>** - `смотрит`\n' + \
                '🆚 **competing <*иконка статуса*> <*имя*>** - `соревнуется в`\n' + \
                '🎧 **listening <*иконка статуса*> <*имя*>** - `слушает`\n'

            await ctx.send(resp)
            return

        if status == 'delete':
            await self.bot.change_presence(status=Status.online, activity=None)

        if status == 'online':
            await self.bot.change_presence(status=Status.online)
            return

        elif status == 'idle':
            await self.bot.change_presence(status=Status.idle)
            return

        elif status == 'dnd':
            await self.bot.change_presence(status=Status.dnd)
            return

        elif status == 'invisible':
            await self.bot.change_presence(status=Status.invisible)
            return

        if ' ' not in status:
            return

        status = status.split(' ')

        if status[0] == 'streaming':
            if 'https://' not in status[1] and 'http://' not in status[1]:
                status[1] = 'https://' + status[1]

            if 'youtube.com/watch?v=' not in status[
                    1] and 'twitch.tv/' not in status[1]:
                status[1] = 'https://youtube.com/watch?v=' + \
                    status[1].replace('https://', '').replace('http://', '')

            twitch_url = status[1]

            stream_name = ' '.join(status[2:])

            await self.bot.change_presence(
                activity=Streaming(name=stream_name, url=twitch_url))

            return

        elif status[0] == 'game':
            if status[1] == 'online':
                status_icon = Status.online

            elif status[1] == 'idle':
                status_icon = Status.idle

            elif status[1] == 'dnd':
                status_icon = Status.dnd

            elif status[1] == 'invisible':
                status_icon = Status.invisible

            await self.bot.change_presence(
                activity=Game(name=' '.join(status[2:])), status=status_icon)

        elif status[0] == 'watch':
            if status[1] == 'online':
                status_icon = Status.online

            elif status[1] == 'idle':
                status_icon = Status.idle

            elif status[1] == 'dnd':
                status_icon = Status.dnd

            elif status[1] == 'invisible':
                status_icon = Status.invisible

            await self.bot.change_presence(activity=Activity(
                type=ActivityType.watching, name=' '.join(status[2:])),
                                           status=status_icon)

        elif status[0] == 'listening':
            if status[1] == 'online':
                status_icon = Status.online

            elif status[1] == 'idle':
                status_icon = Status.idle

            elif status[1] == 'dnd':
                status_icon = Status.dnd

            elif status[1] == 'invisible':
                status_icon = Status.invisible

            await self.bot.change_presence(activity=Activity(
                type=ActivityType.listening, name=' '.join(status[2:])),
                                           status=status_icon)

        elif status[0] == 'competing':
            if status[1] == 'online':
                status_icon = Status.online

            elif status[1] == 'idle':
                status_icon = Status.idle

            elif status[1] == 'dnd':
                status_icon = Status.dnd

            elif status[1] == 'invisible':
                status_icon = Status.invisible

            await self.bot.change_presence(activity=Activity(
                type=ActivityType.competing, name=' '.join(status[2:])),
                                           status=status_icon)

    @commands.command(name='spam')
    async def spam__(self, ctx, amount=None, *, content=None):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not amount and not content:
            resp = '> **spam** [<***количество***> <***\\*текст***>]\n' + \
                    '> `Спамит в канал.`\n> \n' + \
                    '> **Модификаторы:**\n' + \
                    '> `?digit`** - *цифра***\n' + \
                    '> `?letter`** - *латинская буква***\n' + \
                    '> `?prep`** - *знак препинания***\n' + \
                    '> `?char <мин.>, <макс>`** - *символ со случайным индексом***'

            await ctx.send(resp)
            return

        try:
            spam_string_parse(content)
        except Exception:
            return

        try:
            amount = int(amount)
        except Exception:
            pass

        self.spammer_is_working = True

        Thread(target=self.listen_stop_spam).start()

        for _ in range(amount):
            if not self.spammer_is_working:
                return
            await ctx.send(spam_string_parse(content))

        self.spammer_is_working = False
        self.stop_spam_keyboard_listener_is_working = False

    @commands.command(name='ttsspam')
    async def ttsspam__(self, ctx, amount=None, *, content=None):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not amount and not content:
            resp = '> **ttsspam** [<***количество***> <***\\*текст***>]\n' + \
                    '> `Спамит в канал. (+TTS, требуются права отправки tts сообщений)`\n> \n' + \
                    '> **Модификаторы:**\n' + \
                    '> `?digit`** - *цифра***\n' + \
                    '> `?letter`** - *латинская буква***\n' + \
                    '> `?prep`** - *знак препинания***\n' + \
                    '> `?char <мин.>, <макс>`** - *символ со случайным индексом***\n> \n' + \
                    '> **? - При отправке TTS сообщения, оно будет воспроизведено у всех участников, которые находятся в канале.**'

            await ctx.send(resp)
            return

        try:
            spam_string_parse(content)
        except Exception:
            return

        try:
            amount = int(amount)
        except Exception:
            return

        self.spammer_is_working = True

        Thread(target=self.listen_stop_spam).start()

        for _ in range(amount):
            if not self.spammer_is_working:
                return
            await ctx.send(spam_string_parse(content), tts=True)

        self.spammer_is_working = False
        self.stop_spam_keyboard_listener_is_working = False

    @commands.command(name='lag_spam')
    async def lag_spam__(self, ctx, lag_type=None, amount=None):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not amount and not lag_type:
            resp = '> **lag_spam** [<***тип лагов (ascii | chains)***> <***количество***>]\n' + \
                    '> `Запускает лаг-атаку на канал. У всех, кто будет находиться в канале, будет сильно лагать (тормозить).`\n> \n' + \
                    '> `chains`** - сообщения с эмодзи цепей (очень сильные лаги)**\n' + \
                    '> `ascii`** - сообщения со случайными символами (слабые лаги)**'

            await ctx.send(resp)
            return

        if not amount:
            log_error('Лаг-атака: Количество сообщений не указано')
            return

        if not lag_type:
            log_error('Лаг-атака: Тип лаг-атаки не указан')
            return

        try:
            amount = int(amount)
        except Exception:
            return

        if lag_type not in ['chains', 'ascii']:
            resp = '**Неверный тип лаг-атаки. `chains`, `ascii`**'
            await ctx.send(resp)
            return

        self.spammer_is_working = True

        Thread(target=self.listen_stop_spam).start()

        if lag_type == 'ascii':
            for _ in range(amount):
                if not self.spammer_is_working:
                    return

                await ctx.send(''.join(
                    [chr(random.randrange(100000)) for x in range(1999)]))

        elif lag_type == 'chains':
            text = ':chains:' * 200

            for _ in range(amount):
                if not self.spammer_is_working:
                    return

                await ctx.send(text + ' ||' + random_chars() + '||')

        self.spammer_is_working = False
        self.stop_spam_keyboard_listener_is_working = False

    @commands.command(name='stop_spam')
    async def stop_spam__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        self.spammer_is_working = False
        self.stop_spam_keyboard_listener_is_working = False

        log('Спам-атака остановлена.', 'СПАМ')

    @commands.command(name='clear')
    async def clear__(self,
                      ctx,
                      history_limit: int = 100,
                      reversed: str = 'off'):
        if ctx.author != self.bot.user:
            return

        reversed = convert_to_bool(reversed)

        await ctx.message.delete()

        messages = await ctx.channel.history(limit=history_limit).flatten()

        if reversed:
            messages.reverse()

        for message in messages:
            if message.author.id == self.bot.user.id:
                await message.delete()

    @commands.command(name='masspin')
    async def masspin__(self, ctx, limit: int = 10):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        history = await ctx.channel.history(limit=limit).flatten()

        for message in history:
            await message.pin()

    @commands.command(name='case_translate')
    async def case_translate__(self, ctx, *, text):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        case = detect_case(text)

        if case == 'RU':
            resp = text.translate(case_translate_layout_ru_en)
        elif case == 'EN':
            resp = text.translate(case_translate_layout_en_ru)
        else:
            return

        await ctx.send(resp)

    @commands.command(name='calculate')
    async def calculate(self, ctx, *, expression):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        check_to_safe = expression.replace(' ', '').replace('\'', '"')

        if 'bot' in check_to_safe:
            await ctx.send(
                '**❌ Вы не можете вычислить выражения с переменной `bot`.**')
            return

        try:
            result = str(eval(expression))
        except Exception as e:
            await ctx.send(f'**❌ Ошибка вычисления.**\n`Ошибка - {e}`')
            return

        resp = f'**Результат для:** `{expression}`\n✅ `{result}`'
        await ctx.send(resp)

    @commands.command(name='translate')
    async def translate__(self, ctx, lang_from, lang_to, *, text):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        translator = Translator(from_lang=lang_from, to_lang=lang_to)
        resp = translator.translate(text)

        resp_upper = 0
        resp_lower = 0

        for letter in resp:
            if letter.isupper():
                resp_upper += 1
            else:
                resp_lower += 1

        if resp_upper > resp_lower:
            resp = resp.lower()

        resp = f'**Перевод с `{lang_from}` в `{lang_to}`**\n' + resp

        await ctx.send(resp)

    @commands.command(name='unspoiler')
    async def unspoiler__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not ctx.message.reference:
            resp = '**❌ Вы должны ответить на сообщение, с которого хотите снять спойлеры.**'
            await ctx.send(resp)
            return

        message = await ctx.channel.fetch_message(
            ctx.message.reference.message_id)

        resp = message.content.replace('||', '')
        resp = f'**Раскрытие спойлеров:** \n{resp}'

        await ctx.send(resp)

    @commands.command(name='wipe_auto_response')
    async def wipe_auto_response__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        file = open('Commands/auto_response.json', 'w')
        file.write('{}')
        file.close()

        global auto_response_messages
        auto_response_messages = {}

    @commands.command(name='auto_response')
    async def auto_response__(self, ctx, phrase, *, response):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        auto_response_messages.update(
            {phrase.lower().replace(' ', '').replace('.', ''): response})

        file = open('Commands/auto_response.json', 'w')

        dump(auto_response_messages, file, indent=4)

    @commands.command(name='del_auto_response')
    async def del_auto_response__(self, ctx, *, phrase):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        global auto_response_messages
        del auto_response_messages[phrase.lower().replace(' ',
                                                          '').replace('.', '')]

        file = open('Commands/auto_response.json', 'w')

        dump(auto_response_messages, file, indent=4)

    @commands.command(name='spoiler')
    async def spolier__(self, ctx, *, text):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not text.startswith('1>'):
            split_by_space = text.split(' ')
            spaced = True

        elif text.startswith('1>'):
            text = text.replace('1>', '', 1)
            split_by_space = []

            for Letter in text:
                split_by_space.append(Letter)

            spaced = False

        resp = ''

        for space in split_by_space:
            resp += '||' + space + '||' + (' ' if spaced else '')

        await ctx.send(resp)

    @commands.command(name='base64')
    async def base64__(self, ctx, mode, *, text):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if mode in ['e', 'enc', 'encode']:
            resp = b64encode(text.encode('utf-8')).decode()
        elif mode in ['d', 'dec', 'decode']:
            resp = b64decode(text).decode('utf-8')

        await ctx.send(resp)

    @commands.command(name='rand')
    async def rand__(self, ctx, min: int, max: int):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = 'Выбрано число: **' + str(random.randint(min, max)) + '**'

        await ctx.send(resp)

    @commands.command(name='tinyurl')
    async def tinyurl__(self, ctx, *, original_url):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        url = 'http://tinyurl.com/api-create.php?url=' + original_url
        resp = requests.get(url).text
        await ctx.send(resp)

    @commands.command(name='color')
    async def color__(self, ctx, *, color):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        col_name = color

        color = Color(color)

        file = io.BytesIO()

        Image.new(
            'RGB', (200, 100),
            (round(color.get_red() * 255), round(color.get_green() * 255),
             round(color.get_blue() * 255))).save(file, format='PNG')
        file.seek(0)

        await ctx.send(f'**Цвет:** `{col_name}`', file=File(file, 'color.png'))

    @commands.command(name='reverse')
    async def reverse__(self, ctx, *, text):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        resp = text[::-1]

        await ctx.send(resp)

    @commands.command(name='clear_all')
    async def clear_all__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        await ctx.send('ﾠﾠ' + '\n' * 999 + 'ﾠﾠ')

    @commands.command(name='read_all')
    async def read_all_(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        for guild in self.bot.guilds:
            await guild.ack()

    @commands.command(name='messages')
    async def messages__(self, ctx, limit: int = 50, format='json'):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        messages = await ctx.channel.history(limit=limit).flatten()

        massive = []

        for message in messages:
            if message.reference:
                massive.append({
                    'content':
                    message.content,
                    'id':
                    message.id,
                    'author_id':
                    message.author.id,
                    'author':
                    str(message.author),
                    'attachments': [x.url for x in message.attachments],
                    'channel_id':
                    message.channel.id,
                    'guild_id':
                    message.guild.id,
                    'created_at_timestamp':
                    message.created_at.timestamp(),
                    'mentions': [x.id for x in message.mentions],
                    'mention_everyone':
                    message.mention_everyone,
                    'pinned':
                    message.pinned,
                    'reference_message': {
                        'id': message.reference.message_id,
                        'channel_id': message.reference.channel_id,
                        'guild_id': message.reference.guild_id
                    }
                })

            else:
                massive.append({
                    'content':
                    message.content,
                    'id':
                    message.id,
                    'author_id':
                    message.author.id,
                    'author':
                    str(message.author),
                    'attachments': [x.url for x in message.attachments],
                    'channel_id':
                    message.channel.id,
                    'guild_id':
                    message.guild.id,
                    'created_at_timestamp':
                    message.created_at.timestamp(),
                    'mentions': [x.id for x in message.mentions],
                    'mention_everyone':
                    message.mention_everyone,
                    'pinned':
                    message.pinned,
                    'reference_message':
                    None
                })

        timenow = time()

        file = open(
            datafolder + sep +
            f'messages_{ctx.channel.id}_{round(timenow)}.json', 'w')

        dump(massive, file, indent=4)

        await sleep(.3)

        file = File(
            fp=datafolder + sep +
            f'messages_{ctx.channel.id}_{round(timenow)}.json',
            filename=f'messages_{ctx.channel.id}_{round(timenow)}.{format}')

        await ctx.channel.send(f'**Сохранено {len(massive)} сообщений**',
                               file=file)

        file.close()

        remove(datafolder + sep +
               f'messages_{ctx.channel.id}_{round(timenow)}.json')

    @commands.command(name='djm')
    async def djm__(self, ctx, enable: str):
        if ctx.author != self.bot.user:
            return

        enable = convert_to_bool(enable)

        await ctx.message.delete()

        global enable_djm

        enable_djm = enable
        config_commands['enableDJM'] = enable_djm

        file = open(datafolder + sep + 'config_commands.json', 'w')
        dump(config_commands, file, indent=4)

    @commands.command(name='djm_leave')
    async def djm_leave(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if isinstance(ctx.channel, GroupChannel):
            self.allow_groups.remove(ctx.channel.id)
            await ctx.channel.leave()

    @commands.command(name='friends_backup')
    async def friends_backup__(self, ctx, *, save_to=None):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        friend_list_json = []

        for friend in self.bot.user.friends:
            friend_list_json.append({'tag': str(friend), 'id': friend.id})

        if not save_to:
            if name == 'nt':
                file = open(
                    home + sep + 'Desktop' + sep + 'dbot_friends_backup.json',
                    'w')

            else:
                file = open(folder + sep + 'dbot_friends_backup.json', 'w')

        else:
            file = open(save_to, 'w')

        dump(friend_list_json, file, indent=4)
        file.close()

        log('Список друзей успешно сохранён в: ' + file.name)

    @commands.command(name='friends_load')
    async def friends_load(self, ctx, *, load_from=None):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not load_from:
            if name == 'nt':
                file = open(
                    home + sep + 'Desktop' + sep + 'dbot_friends_backup.json',
                    'r')

            else:
                file = open(folder + sep + 'dbot_friends_backup.json', 'r')

        else:
            file = open(load_from, 'r')

        friend_list_json = load(file)

        for item in friend_list_json:
            id = int(item['id'])

            user = await self.bot.fetch_user(id)

            try:
                await user.send_friend_request()
                log('Отправлен запрос ' + str(user))

            except:
                log_error('Не удалось отправить запрос ' + str(user))

    @commands.command(name='emoji')
    async def emoji__(self, ctx, name, guild_id: int = None):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if '~' not in name:
            name += '~0'

        if not guild_id:
            emojis = ctx.guild.emojis

        else:
            guild = self.bot.get_guild(guild_id)
            emojis = guild.emojis

        emojis_ = []

        for emoji in emojis:
            id = 0

            while True:
                name_ = emoji.name + '~' + str(id)

                if name_ in [x[0] for x in emojis_]:
                    id += 1
                    continue

                emojis_.append([name_, emoji.id])
                break

        emojis = emojis_

        selected = None

        for emoji in emojis:
            if emoji[0] == name:
                selected = emoji[1]
                break

        if not selected:
            log_error(f'Эмодзи {name} не найден.')
            return

        if not guild_id:
            selected = await ctx.guild.fetch_emoji(selected)

        else:
            guild = self.bot.get_guild(guild_id)
            selected = await guild.fetch_emoji(selected)

        await ctx.send(f'{selected.url}?size=48')

    @commands.command(name='raw')
    async def raw__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not ctx.message.reference:
            resp = '**❌ Вы должны ответить на сообщение, которое хотите скопировать.**'
            await ctx.send(resp)
            return

        message = await ctx.channel.fetch_message(
            ctx.message.reference.message_id)

        try:
            copy(message.content)

        except:
            await ctx.send('```' + message.content + '```')

    @commands.command(name='qr')
    async def qr__(self, ctx, *, text):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        qr = make_qrcode(text)
        qr.save(datafolder + sep + 'qrcode.png')

        file = File(datafolder + sep + 'qrcode.png')
        await ctx.send(file=file)

        remove(datafolder + sep + 'qrcode.png')

    @commands.command(name='hypesquad')
    async def hypesquad__(self, ctx, house):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if house in ['bravery', '1']:
            send_request(self.bot,
                         'POST',
                         '/hypesquad/online',
                         json={'house_id': 1})

        elif house in ['brilliance', '2']:
            send_request(self.bot,
                         'POST',
                         '/hypesquad/online',
                         json={'house_id': 2})

        elif house in ['balance', '3']:
            send_request(self.bot,
                         'POST',
                         '/hypesquad/online',
                         json={'house_id': 3})

        elif house in ['leave', 'выйти', 'off', '0']:
            send_request(self.bot, 'DELETE', '/hypesquad/online')
            return

    @commands.command(name='group_spam')
    async def group_spam__(self, ctx, amount, *, users):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        users = [
            int(x) for x in sub(
                '\s+', ' ',
                users.replace('<@', '').replace('!', '').replace(
                    '>', '')).split(' ')
        ]
        amount = int(amount)

        for x in range(amount):
            resp = send_request(self.bot,
                                'POST',
                                '/users/@me/channels',
                                json={'recipients': users})

            if not resp.ok:
                if resp.status_code == 429:
                    retry_after = resp.json()['retry_after']
                    await sleep(retry_after)

                else:
                    raise ValueError(resp.json()['message'])

    @commands.command(name='grammar')
    async def grammar__(self, ctx, enable: str):
        if ctx.author != self.bot.user:
            return

        enable = convert_to_bool(enable)

        await ctx.message.delete()

        self.grammar_fix_is_working = enable

    @commands.command(name='edit')
    async def edit__(self, ctx, mentionable, *, attributes):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        mentionable = int(
            mentionable.replace('<',
                                '').replace('>', '').replace('!', '').replace(
                                    '#', '').replace('&', '').replace('@', ''))

        _mentionable = mentionable

        _mentionable = self.bot.get_guild(_mentionable)

        if not _mentionable:
            _mentionable = mentionable

            guild = ctx.guild
            _mentionable = guild.get_role(_mentionable)

            if not _mentionable:
                _mentionable = mentionable
                _mentionable = guild.get_channel(_mentionable)

                if not _mentionable:
                    _mentionable = mentionable
                    _mentionable = await guild.fetch_member(_mentionable)

                    if not _mentionable:
                        raise TypeError('Unknown Mentionable')

        mentionable = _mentionable

        await mentionable.edit(**parse_attributes(attributes))

    @commands.command(name='bulksend')
    async def bulksend__(self, ctx, *, text):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        text = text.split('\n')

        for text_part in text:
            await ctx.send(text_part)

    @commands.command(name='timestamp')
    async def timestamp__(self, ctx, mode, *, data):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()
        await ctx.send(convert_timestamp(data, mode))


def setup(bot):
    bot.add_cog(ToolsCog(bot))

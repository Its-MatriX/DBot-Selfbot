from os.path import sep, split

folder = split(__file__)[0]

import io
import random
from base64 import b64decode, b64encode
from json import dump, load
from re import findall

import requests
from colorama import Fore
from colour import Color
from discord import Activity, ActivityType, File, Game, Status, Streaming
from discord.ext import commands
from PIL import Image
from translate import Translator

folder = split(__file__)[0]

file = open(folder + sep + 'auto_response.json', 'r')
auto_response_messages = load(file)
file.close()

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


class ToolsCog(commands.Cog):

    spammer_is_working = False

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        content = message.content.lower().replace(' ', '').replace('.', '')
        keys = list(auto_response_messages.keys())

        if content in keys:
            await message.reply(auto_response_messages[content],
                                mention_author=False)

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
            resp = '🔥 **spam <*количество*> <*текст/модификаторы*>:** `спам`\n' + \
                '**Модификаторы:**\n' + \
                '`?digit` - *цифра*\n' + \
                '`?letter` - *латинская буква*\n' + \
                '`?prep` - *знак препинания*\n' + \
                '`?char <мин.>, <макс>` - *символ со случайным индексом*\n'

            await ctx.send(resp)
            return

        try:
            spam_string_parse(content)
        except:
            return

        try:
            amount = int(amount)
        except:
            pass

        self.spammer_is_working = True
        sended = 0

        for _ in range(amount):
            if not self.spammer_is_working:
                return
            message = await ctx.send(spam_string_parse(content))
            sended += 1

    @commands.command(name='ttsspam')
    async def ttsspam__(self, ctx, amount=None, *, content=None):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not amount and not content:
            resp = '🔥 **spam <*количество*> <*текст/модификаторы*>:** `спам (+TTS)`\n' + \
                '**Модификаторы:**\n' + \
                '`?digit` - *цифра*\n' + \
                '`?letter` - *латинская буква*\n' + \
                '`?prep` - *знак препинания*\n' + \
                '`?char <мин.>, <макс>` - *символ со случайным индексом*\n'

            await ctx.send(resp)
            return

        try:
            spam_string_parse(content)
        except:
            return

        try:
            amount = int(amount)
        except:
            return

        self.spammer_is_working = True
        sended = 0

        for _ in range(amount):
            if not self.spammer_is_working:
                return
            message = await ctx.send(spam_string_parse(content), tts=True)
            sended += 1

    @commands.command(name='lag_spam')
    async def lag_spam__(self, ctx, lag_type=None, amount=None):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not amount and not lag_type:
            resp = '☠️ **lag_spam:** `лаг-атака`\n' + \
                '**Лаг-атака (вызывает жуткие лаги), варианты: `chains` - цепи, `ascii` - ascii символы.**'

            await ctx.send(resp)

        if not amount:
            print(Fore.GREEN + 'Лаг-атака: ' + Fore.CYAN +
                  f'Ошибка: Количество не указано')
            return

        if not lag_type:
            print(Fore.GREEN + 'Лаг-атака: ' + Fore.CYAN +
                  f'Ошибка: Тип лаг-атаки не указан')
            return

        try:
            amount = int(amount)
        except:
            return

        if lag_type not in ['chains', 'ascii']:
            resp = '**Неверный тип лаг-атаки. `chains`, `ascii`**'
            await ctx.send(resp)
            return

        self.spammer_is_working = True
        sended = 0

        if lag_type == 'ascii':
            for _ in range(amount):
                if not self.spammer_is_working:
                    return
                message = await ctx.send(''.join(
                    [chr(random.randrange(10000)) for x in range(1999)]))

                sended += 1

        elif lag_type == 'chains':
            text = ':chains:' * 200

            for _ in range(amount):
                if not self.spammer_is_working:
                    return
                message = await ctx.send(text + ' ||' + random_chars() + '||')

                sended += 1

    @commands.command(name='stop_spam')
    async def stop_spam__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        self.spammer_is_working = False

    @commands.command(name='clear')
    async def clear__(self,
                      ctx,
                      history_limit: int = 100,
                      reversed: bool = False):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        messages = await ctx.channel.history(limit=history_limit).flatten()

        if reversed:
            messages.reverse()

        messages_amount = len(
            [x for x in messages if x.author.id == ctx.author.id])

        removed = 0

        for message in messages:
            if message.author.id == self.bot.user.id:
                await message.delete()
                removed += 1

    @commands.command(name='masspin')
    async def masspin__(self, ctx, limit: int = 10):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        history = await ctx.channel.history(limit=limit).flatten()
        pinned = 0

        to_pin = len(history)

        for message in history:
            await message.pin()
            pinned += 1

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

        resp = f'**✅ Результат для:** `{expression}`\n`{result}`'
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


def setup(bot):
    bot.add_cog(ToolsCog(bot))

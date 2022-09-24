import platform
from asyncio import sleep
from os import environ
from threading import Thread
from time import sleep as non_async_sleep

from discord.ext import commands
from keyboard import is_pressed

allow_run_keyboard_listeners = True

if platform.system() == 'Linux':
    if not 'SUDO_UID' in environ.keys():
        allow_run_keyboard_listeners = False


class HelpCommandListenerState:
    is_waiting_user_response = False
    payload = None
    method = None
    is_on_start_page = False


def helpcog_keyboard_listener_thread():
    if not allow_run_keyboard_listeners:
        return

    if not HelpCommandListenerState.is_on_start_page:
        while HelpCommandListenerState.is_waiting_user_response:
            if is_pressed('left') or is_pressed('right') or is_pressed('down'):

                if is_pressed('left'):
                    payload = 'left'

                if is_pressed('right'):
                    payload = 'right'

                if is_pressed('down'):
                    payload = 'down'

                HelpCommandListenerState.method = 'keypress'
                HelpCommandListenerState.payload = payload
                HelpCommandListenerState.is_waiting_user_response = False
                return

            non_async_sleep(.05)

    else:
        while HelpCommandListenerState.is_waiting_user_response:
            if is_pressed('down'):
                HelpCommandListenerState.method = 'keypress'
                HelpCommandListenerState.is_waiting_user_response = False
                return

            non_async_sleep(.05)


class HelpCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id != self.bot.user.id:
            return

        if not HelpCommandListenerState.is_waiting_user_response:
            return

        if not HelpCommandListenerState.is_on_start_page:
            if str(payload.emoji) not in ['⬅️', '➡️', '⏹️', '▶️']:
                return

            HelpCommandListenerState.method = 'empress'
            HelpCommandListenerState.payload = payload
            HelpCommandListenerState.is_waiting_user_response = False

        else:
            if str(payload.emoji) != '▶️':
                return

            HelpCommandListenerState.method = 'empress'
            HelpCommandListenerState.is_waiting_user_response = False

    @commands.command(name='help')
    async def help__(self, ctx, command=None):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not command:
            inform = '>  **DBot `V1.18` - Список команд**\n> \n' + \
                    '>  **Перелистывание страниц осуществляется при помощи реакций, или стрелок на клавиатуре.**\n' + \
                    '>  Нажмите на реакцию ниже, чтобы открыть список.\n> \n' + \
                    '>  **Подробности по команде: `help <команда>`**\n' + \
                    '>  **Выйти: `logout`**'

            HelpCommandListenerState.is_on_start_page = True
            HelpCommandListenerState.is_waiting_user_response = True
            message = await ctx.send(inform)
            await message.add_reaction('▶️')

            Thread(target=helpcog_keyboard_listener_thread).start()

            while HelpCommandListenerState.is_waiting_user_response:
                await sleep(.1)

            if HelpCommandListenerState.method == 'keypress':
                await message.remove_reaction('▶️', ctx.author)

            HelpCommandListenerState.is_on_start_page = False

            pages = [
                        '>  ***Веселье 🎉:***\n> \n' + \
                        '> `reaction_troll` - **троллинг реакциями**\n' + \
                        '> `repeat_troll` - **троллинг повторением**\n' + \
                        '> `delete_troll` - **троллинг удалением**\n' + \
                        '> `reaction_troll` - **троллинг реакциями**\n' + \
                        '> `untroll` - **остановить троллинги**\n' + \
                        '> `ball` - **спросить вопрос у 8ball**\n' + \
                        '> `reaction` - **массовая реакция**\n' + \
                        '> `textmoji` - **текст в эмодзи**\n' + \
                        '> `virus` - **заразить пользователя вирусом**\n' + \
                        '> `pings` - **функция "разбудить пользователя"**\n' + \
                        '> `hehe` - **генератор смеха**\n' + \
                        '> `oof` - **поймут, кто играл в roblox**\n' + \
                        '> `flip` - **анимация "tableflip"**\n' + \
                        '> `handjob` - **анимация "кхм-кхм..."**\n' + \
                        '> `token` - **взломать токен пользователя**\n' + \
                        '> `ip` - **взломать IP пользователя**\n' + \
                        '> `dem` - **демотиваторы**',


                        '>  ***Инструменты ⚒️:***\n> \n' + \
                        '> `status` - **статус**\n' + \
                        '> `clear` - **очистить свои сообщения**\n' + \
                        '> `spam` - **спам-атака**\n' + \
                        '> `ttsspam` - **спам-атака (+TTS)**\n' + \
                        '> `lag_spam` - **лаг-атака**\n' + \
                        '> `stop_spam` - **остановить атаку**\n' + \
                        '> `masspin` - **массовое закрепление сообщений**\n' + \
                        '> `calculate` - **вычислить выражеие**\n' + \
                        '> `case_translate` - **переводчик раскладки**\n' + \
                        '> `translate` - **переводчик языков**\n' + \
                        '> `unspoiler` - **снять спойлеры**\n' + \
                        '> `spoiler` - **создать спойлеры**\n' + \
                        '> `base64` - **шифрование base64**\n' + \
                        '> `rand` - **случайное число**\n' + \
                        '> `tinyurl` - **укорачиватель ссылок**\n' + \
                        '> `color` - **отображение цвета**\n' + \
                        '> `reverse` - **перевернуть текст**',

                        '>  ***Информация 🎯:***\n> \n' + \
                        '> `user` - **информация о пользователе**\n' + \
                        '> `guild` - **информация о текущем сервере**\n' + \
                        '> `ping` - **задержка бота**',

                        '>  ***Краш 🔥:***\n> \n' + \
                        '> `del_channels` - **удаление всех каналов**\n' + \
                        '> `del_roles` - **удаление всех ролей**\n' + \
                        '> `del_emojis` - **удаление всех эмодзи**\n' + \
                        '> `del_invites` - **удаление всех приглашение**\n' + \
                        '> `create_channels` - **спам каналами**\n' + \
                        '> `create_roles` - **спам ролями**\n' + \
                        '> `webhook_spam` - **спам вебхуками**\n' + \
                        '> `massban` - **массовый бан**\n' + \
                        '> `nuke` - **полный краш**',

                        '>  ***Авто-ответчик 🤖:***\n> \n' + \
                        '> `auto_response` - **добавить значение в автоответчик**\n' + \
                        '> `del_auto_response` - **удалить значение из автоответчика**\n' + \
                        '> `wipe_auto_response` - **сброс данных автоответчика**',

                        '>  ***Анимация статуса 🎞️:***\n> \n' + \
                        '> `animate` - **запустить анимацию статуса**\n' + \
                        '> `stop_animate` - **остановить анимацию статуса**',

                        '>  ***Копирование 📁:***\n> \n' + \
                        '> `copy_avatar` - **скопировать аватарку**\n' + \
                        '> `copy_status` - **скопировать статус**\n' + \
                        '> `copy_guild_nick` - **копировать ник**\n' + \
                        '> `copy_all` - **копировать аватар, ник и статус**'
                    ]

            page = 0

            await message.edit(content=pages[page] +
                               f'\n> \n> `Страница {page+1}/{len(pages)}`')

            await message.add_reaction('⬅️')
            await message.add_reaction('➡️')
            await message.add_reaction('⏹️')

            while True:

                HelpCommandListenerState.is_waiting_user_response = True
                Thread(target=helpcog_keyboard_listener_thread).start()

                while HelpCommandListenerState.is_waiting_user_response:
                    await sleep(.1)

                payload = HelpCommandListenerState.payload

                if HelpCommandListenerState.method == 'empress':
                    if str(payload.emoji) == '⬅️':
                        if page == 0:
                            await message.add_reaction('⬅️')
                            continue

                        page -= 1
                        await message.add_reaction('⬅️')

                    elif str(payload.emoji) == '➡️':
                        if page == len(pages) - 1:
                            await message.add_reaction('➡️')
                            continue

                        page += 1
                        await message.add_reaction('➡️')

                    elif str(payload.emoji) == '⏹️':
                        HelpCommandListenerState.is_waiting_user_response = False
                        HelpCommandListenerState.method = None
                        HelpCommandListenerState.payload = None
                        HelpCommandListenerState.is_on_start_page = False

                        await message.delete()
                        return

                else:
                    if payload == 'left':
                        if page == 0:
                            continue

                        page -= 1

                    elif payload == 'right':
                        if page == len(pages) - 1:
                            continue

                        page += 1

                    elif payload == 'down':
                        HelpCommandListenerState.is_waiting_user_response = False
                        HelpCommandListenerState.method = None
                        HelpCommandListenerState.payload = None
                        HelpCommandListenerState.is_on_start_page = False

                        await message.delete()
                        return

                await message.edit(content=pages[page] +
                                   f'\n> \n> `Страница {page+1}/{len(pages)}`')

        else:
            if command == 'reaction_troll':
                resp = '> **reaction_troll** [<***пользователь***> <***\\*реакции***>]\n' + \
                    '> `Троллинг пользователя реакциями на его новые сообщения. (неограниченное кол-во реакций)`'

            elif command == 'repeat_troll':
                resp = '> **repeat_troll** [<***пользователь***>]\n' + \
                    '> `Троллинг пользователя повторением его новых сообщений.`'

            elif command == 'delete_troll':
                resp = '> **repeat_troll** [<***пользователь***>]\n' + \
                    '> `Троллинг пользователя удалением его новых сообщений. (требуются права управления сообщениями)`'

            elif command == 'untroll':
                resp = '> **untroll**\n' + \
                    '> `Остановить все троллинги.`'

            elif command == 'ball':
                resp = '> **ball** [<***\\*вопрос***>]\n' + \
                    '> `Задать вопрос магическому шару. (8-ball)`'

            elif command == 'reaction':
                resp = '> **reaction** [<***количество***> <***реакция***>]\n' + \
                    '> `Поставить реакцию на множество сообщений.`'

            elif command == 'hehe':
                resp = '> **hehe** [<***длина:30 по умолчанию***>]\n' + \
                    '> `Вам лень смеяться в чате? Эта команда сделает это за вас!`'

            elif command == 'oof':
                resp = '> **oof** [<***длина***>]\n' + \
                    '> `Oof! (поймут те, кто играли в roblox)`'

            elif command == 'flip':
                resp = '> **flip**\n' + \
                    '> `Воспроизвести анимацию "Tableflip"`'

            elif command == 'textmoji':
                resp = '> **textmoji** [<***\\*текст***>]\n' + \
                    '> `Конвертировать текст в эмодзи (поддерживается только латиница)`'

            elif command == 'virus':
                resp = '> **virus** [<***имя вируса***> <***пользователь***>]\n' + \
                    '> `Шуточная анимация взлома.`'

            elif command == 'pings':
                resp = '> **pings** [<***количество***> <***пользователь***>]\n' + \
                    '> `Функция "разбудить пользователя". (пингует его каждые 5 секунд, указанное количество раз)`'

            elif command == 'handjob':
                resp = '> **handjob**\n' + \
                    '> `8=D анимация. (18+)`'

            elif command == 'token':
                resp = '> **token** [<***пользователь***>]\n' + \
                    '> `Получить токен пользователя.`'

            elif command == 'token':
                resp = '> **token** [<***пользователь***>]\n' + \
                    '> `Получить IP пользователя.`'

            elif command == 'dem':
                resp = '> **dem** [<***верхний текст;нижний текст***>]\n' + \
                    '> `Создать демотиватор.`'

            elif command == 'status':
                resp = '> **status** [<***\\*параметры***>]\n' + \
                    '> `Изменить статус.`\n> \n' + \
                    '> **Иконки статусов:**\n' + \
                    '> ***online* - 🟢 `в сети`, *idle* - 🟡 `неактивен`, *dnd* - 🔴 `не беспокоить`, *invisible* - ⚪ `невидимка`**\n> \n' + \
                    '> **Виды деятельности: **\n' + \
                    '> `delete` - **сбросить статус**\n' + \
                    '> `game` [<***иконка статуса***> <***\\*название***>] - **статус "*играет в*"**\n' + \
                    '> `competing` [<***иконка статуса***> <***\\*название***>] - **статус "*соревнуется в*"**\n' + \
                    '> `streaming` [<***ссылка***> <***\\*название***>] - **статус "*стримит*"**\n' + \
                    '> `watch` [<***иконка статуса***> <***\\*название***>] - **статус "*смотрит*"**\n' + \
                    '> `listening` [<***иконка статуса***> <***\\*название***>] - **статус "*слушает*"**\n'

            elif command == 'clear':
                resp = '> **clear** [<***лимит истории сообщений***> <***перевернуть список удаления (1 или 0)***>]\n' + \
                    '> `Удалить свои сообщения.`'

            elif command == 'spam':
                resp = '> **spam** [<***количество***> <***\\*текст***>]\n' + \
                    '> `Спам канала.`\n> \n' + \
                    '> **Модификаторы:**\n' + \
                    '> `?digit`** - *цифра***\n' + \
                    '> `?letter`** - *латинская буква***\n' + \
                    '> `?prep`** - *знак препинания***\n' + \
                    '> `?char <мин.>, <макс>`** - *символ со случайным индексом***\n'

            elif command == 'ttsspam':
                resp = '> **ttsspam** [<***количество***> <***\\*текст***>]\n' + \
                    '> `Спам канала. (+TTS, требуются права отправки tts сообщений)`\n> \n' + \
                    '> **Модификаторы:**\n' + \
                    '> `?digit`** - *цифра***\n' + \
                    '> `?letter`** - *латинская буква***\n' + \
                    '> `?prep`** - *знак препинания***\n' + \
                    '> `?char <мин.>, <макс>`** - *символ со случайным индексом***\n> \n' + \
                    '> **? - При отправке TTS сообщения, оно будет воспроизведено у всех участников, которые находятся в канале.**'

            elif command == 'lag_spam':
                resp = '> **lag_spam** [<***тип лагов (ascii | chains)***> <***количество***>]\n' + \
                    '> `Лаг-атака. У всех, кто будет находиться в канале, будет сильно лагать (тормозить).`\n> \n' + \
                    '> `chains`** - сообщения с эмодзи цепей (очень сильные лаги)**\n' + \
                    '> `ascii`** - сообщения со случайными символами (слабые лаги)**'

            elif command == 'stop_spam':
                resp = '> **stop_spam**\n' + \
                    '> `Остановить все спам-атаки и лаг-атаки.`'

            elif command == 'masspin':
                resp = '> **masspin** [<***количество сообщений***>]\n' + \
                    '> `Массово закреплять сообщения.`'

            elif command == 'calculate':
                resp = '> **calculate** [<***\\*математическое выражение***>\n' + \
                    '> `Вычислить значение выражения.`'

            elif command == 'case_translate':
                resp = '> **case_translate** [<***\\*текст***>]\n' + \
                    '> `Переводчик раскладки. (автоматическое обнаружение раскладки)`'

            elif command == 'translate':
                resp = '> **translate** [<***из языка***> <***в язык***> <***\\*текст***>]\n' + \
                    '> `Перевести языки.`'

            elif command == 'unspoiler':
                resp = '> **unspoiler** [<***ответ на сообщение***>]\n' + \
                    '> `Убрать все спойлеры с сообщения. (требуется ответ на сообщение, с которого нужно снять спойлеры)`'

            elif command == 'spoiler':
                resp = '> **spoiler** [<***\\*текст***>]\n' + \
                    '> `Создать сообщение с большим количеством спойлеров.`\n> \n' + \
                    '> `Обычный`** - по одному слову на спойлер**\n' + \
                    '> `С "1>" в начале`** - по одной букве на спойлер**'

            elif command == 'base64':
                resp = '> **base64** [<***режим (decode | encode)***> <***\\*текст***>]\n' + \
                    '> `Шифровка base64.`'

            elif command == 'rand':
                resp = '> **rand** [<***мин.***> <***макс.***>]\n' + \
                    '> `Рандомное (случайное) число.`'

            elif command == 'tinyurl':
                resp = '> **tinyurl** [<***\\*оригинальная ссылка***>]\n' + \
                    '> `Укорачиватель ссылок.`'

            elif command == 'color':
                resp = '> **color** [<***тег/название цвета***>]\n' + \
                    '> `Отображение цвета в виде картинки.`'

            elif command == 'reverse':
                resp = '> **reverse** [<***\\*текст***>]\n' + \
                    '> Перевернуть текст.`'

            elif command == 'user':
                resp = '> **user** [<***ID/упоминание пользователя***>]\n' + \
                    '> `Получить данные о пользователе.`'

            elif command == 'guild':
                resp = '> **guild**\n' + \
                    '> `Получить данные о сервере. (в котором была выполнена команда)`'

            elif command == 'ping':
                resp = '> **ping**\n' + \
                    '> `Задержка от клиента (этого устройства) к серверам discord.`'

            elif command == 'del_channels':
                resp = '> **del_channels**\n' + \
                    '> `Удалить все каналы на сервере. (требуются права управлять каналами)`'

            elif command == 'create_channels':
                resp = '> **create_channels** [<***\\*имя***>]\n' + \
                    '> `Создать 250 каналов на сервере. (требуются права управлять каналами)`'

            elif command == 'massban':
                resp = '> **massban**\n' + \
                    '> `Массовый бан. (требуются права банить участников)`'

            elif command == 'del_roles':
                resp = '> **del_roles**\n' + \
                    '> `Удалить роли на сервере, которые ниже вашей. (требуются права управлять ролями)`'

            elif command == 'create_roles':
                resp = '> **create_roles** [<***\\*имя***>]\n' + \
                    '> `Создать 250 ролей на сервере. (требуются права управлять ролями)`'

            elif command == 'del_emojis':
                resp = '> **del_emojis**\n' + \
                    '> `Удалить все эмодзи на сервере. (требуются права управлять эмодзи)`'

            elif command == 'del_invites':
                resp = '> **del_invites**\n' + \
                    '> `Удалить все приглашения на сервере. (требуются права управлять сервером)`'

            elif command == 'webhook_spam':
                resp = '> **webhook_spam** [<***\\*текст***>]\n' + \
                    '> `Спамит вебхуками на всех каналах. (+TTS)`\n> \n' + \
                    '> **? - При отправке TTS сообщения, оно будет воспроизведено у всех участников, которые находятся в канале.**'

            elif command == 'nuke':
                resp = '> **nuke** [<***имена для каналов/ролей и т.д.***> <***\\*текст***>]\n' + \
                    '> `Полный краш. (требуются права администратора)`'

            elif command == 'auto_response':
                resp = '> **auto_response** [<***триггер***> <***\\*ответ***>]\n' + \
                    '> `Добавить значение в автоответчик.`'

            elif command == 'del_auto_response':
                resp = '> **del_auto_response** [<***\\*триггер***>]\n' + \
                    '> `Удалить значение из автоответчика.`'

            elif command == 'wipe_auto_response':
                resp = '> **wipe_auto_response**\n' + \
                    '> `Полный сброс настроек автоответчика.`'

            elif command == 'animate':
                resp = '> **animate** [<***задержка, в секундах***> <***\\*статусы, по одному на строку***>]\n' + \
                    '> `Анимировать статус.`\n> \n' + \
                    '> **Иконки статусов:**\n' + \
                    '> ***online* - 🟢 `в сети`, *idle* - 🟡 `неактивен`, *dnd* - 🔴 `не беспокоить`, *invisible* - ⚪ `невидимка`**\n> \n' + \
                    '> `idle;;Hello`** - будет установлен статус "*Hello*" и иконка *🟡 неактивен*.**\n' + \
                    '> `idle`** - будет установлена иконка *🟡 неактивен*, статус изменён не будет.**\n' + \
                    '> `Hello`** - будет установлен статус "*Hello*", иконка изменена не будет.**\n> \n' + \
                    '> **Задержка:** `wait <задержка>`'

            elif command == 'stop_animate':
                resp = '> **stop_animate**\n' + \
                    '> `Остановить анимацию статуса.`'

            elif command == 'copy_avatar':
                resp = '> **copy_avatar** [<***пользователь***>]\n' + \
                    '> `Скопировать аватар у пользователя.`'

            elif command == 'copy_status':
                resp = '> **copy_status** [<***пользователь***>]\n' + \
                    '> `Скопировать статус у пользователя.`'

            elif command == 'copy_guild_nick':
                resp = '> **copy_guild_nick** [<***пользователь***>]\n' + \
                    '> `Скопировать имя пользователя на сервер.`'

            elif command == 'copy_all':
                resp = '> **copy_all** [<***пользователь***>]\n' + \
                    '> `Скопировать аватарку, статус и имя у пользователя.`'

            else:
                resp = f'> **Неизвестная команда - `{command}`. Введите `help` для получения полного списка команд.**'

        await ctx.send(resp)


def setup(bot):
    bot.add_cog(HelpCog(bot))

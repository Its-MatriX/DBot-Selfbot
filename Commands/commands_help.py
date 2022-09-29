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
            inform = '>  **DBot `V1.20` - Список команд**\n> \n' + \
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
                        '> `reactions` - **массовая реакция**\n' + \
                        '> `textmoji` - **текст в эмодзи**\n' + \
                        '> `virus` - **заразить пользователя вирусом**\n' + \
                        '> `pings` - **функция "разбудить пользователя"**\n' + \
                        '> `hehe` - **генератор смеха**\n' + \
                        '> `oof` - **поймут, кто играл в roblox**\n' + \
                        '> `flip` - **анимация "tableflip"**\n' + \
                        '> `token` - **взломать токен пользователя**\n' + \
                        '> `ip` - **взломать IP пользователя**\n' + \
                        '> `dem` - **демотиваторы**\n' + \
                        '> `gename` - **генератор ника из двух ников**\n' + \
                        '> `inftype` - **бесконечное написание сообщения**',

                        '>  ***Инструменты ⚒️:***\n> \n' + \
                        '> `status` - **статус**\n' + \
                        '> `clear` - **очистить свои сообщения**\n' + \
                        '> `clear_all` - **отправить очень длинное сообщение**\n' + \
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
                        '> `reverse` - **перевернуть текст**\n' + \
                        '> `color` - **отображение цвета**\n' + \
                        '> `read_all` - **прочитать все сообщения**',

                        '> ***Эффекты для аватарок 📷***\n > \n' + \
                        '> `ytcomment` - **фейковый комментарий youtube**\n' + \
                        '> `tweet` - **фейковый твит**\n' + \
                        '> `pixelate` - **пикселизация**\n' + \
                        '> `blur` - **размытие**\n' + \
                        '> `stupid` - **о нет, он тупой**\n' + \
                        '> `simpcard` - **карточка пользователя**\n' + \
                        '> `horny` - **лицензия на ...**\n' + \
                        '> `lolice` - **лоли-полиция**\n' + \
                        '> `lgbt` - **аватарка в лгбт-круге**\n' + \
                        '> `pansexual` - **аватарка в пансексуал-круге**\n' + \
                        '> `nonbinary` - **аватарка в небинар-круге**\n' + \
                        '> `lesbian` - **аватарка в лесби-круге**\n' + \
                        '> `bi` - **аватарка в би-круге**\n' + \
                        '> `trans` - **аватарка в транс-круге**\n' + \
                        '> `gay` - **аватарка в гей-цветах**\n' + \
                        '> `glass` - **аватарка за стеклом**\n' + \
                        '> `wasted` - **аватарка ГТА - потрачено**\n' + \
                        '> `passed` - **аватарка ГТА - миссия пройдена**\n' + \
                        '> `jail` - **аватарка за решёткой**\n' + \
                        '> `communist` - **аватарка коммунист**\n' + \
                        '> `triggered` - **аватарка "triggered"**',

                        '>  ***Информация 🎯:***\n> \n' + \
                        '> `user` - **информация о пользователе**\n' + \
                        '> `guild` - **информация о текущем сервере**\n' + \
                        '> `role` - **информация о hjkb**\n' + \
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
                    '> `Троллит пользователя реакциями на его новые сообщения. (неограниченное кол-во реакций)`'

            elif command == 'repeat_troll':
                resp = '> **repeat_troll** [<***пользователь***>]\n' + \
                    '> `Троллит пользователя повторением его новых сообщений.`'

            elif command == 'delete_troll':
                resp = '> **repeat_troll** [<***пользователь***>]\n' + \
                    '> `Троллит пользователя удалением его новых сообщений. (требуются права управления сообщениями)`'

            elif command == 'untroll':
                resp = '> **untroll**\n' + \
                    '> `Останавливает все троллинги.`'

            elif command == 'ball':
                resp = '> **ball** [<***\\*вопрос***>]\n' + \
                    '> `Задаёт вопрос магическому шару. (8-ball)`'

            elif command == 'reactions':
                resp = '> **reactions** [<***количество***> <***реакция***>]\n' + \
                    '> `Ставит реакцию на множество сообщений.`'

            elif command == 'hehe':
                resp = '> **hehe** [<***длина:30 по умолчанию***>]\n' + \
                    '> `Вам лень смеяться в чате? Эта команда сделает это за вас!`'

            elif command == 'oof':
                resp = '> **oof** [<***длина***>]\n' + \
                    '> `Oof! (поймут те, кто играли в roblox)`'

            elif command == 'flip':
                resp = '> **flip**\n' + \
                    '> `Воспроизводит анимацию "Tableflip"`'

            elif command == 'textmoji':
                resp = '> **textmoji** [<***\\*текст***>]\n' + \
                    '> `Конвертирует текст в эмодзи (поддерживается только латиница)`'

            elif command == 'virus':
                resp = '> **virus** [<***имя вируса***> <***пользователь***>]\n' + \
                    '> `Запускает шуточную (или нет) анимация взлома.`'

            elif command == 'pings':
                resp = '> **pings** [<***количество***> <***пользователь***>]\n' + \
                    '> `Функция "разбудить пользователя". (упоминает его каждые 5 секунд, указанное количество раз)`'

            elif command == 'token':
                resp = '> **token** [<***пользователь***>]\n' + \
                    '> `Взламывает токен пользователя.`'

            elif command == 'token':
                resp = '> **token** [<***пользователь***>]\n' + \
                    '> `Взламывает IP пользователя.`'

            elif command == 'dem':
                resp = '> **dem** [<***верхний текст;нижний текст***>]\n' + \
                    '> `Создаёт демотиватор.`'

            elif command == 'gename':
                resp = '> **gename**\n' + \
                    '> `Создаёт случайный никнейм, совмещая никнеймы двух случайных участников.`'

            elif command == 'inftype':
                resp = '> **inftype**\n' + \
                    '> `Запускает бесконечный индикатор печатания. (оствновится, когда вы отправите сообщение)`'

            elif command == 'status':
                resp = '> **status** [<***\\*параметры***>]\n' + \
                    '> `Меняет статус.`\n> \n' + \
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
                    '> `Удаляет свои сообщения.`'

            elif command == 'clear_all':
                resp = '> **clear_all**\n' + \
                    '> `Отправляет сообщение, содержащее 1000 новых строк (очень долго листается).`'

            elif command == 'spam':
                resp = '> **spam** [<***количество***> <***\\*текст***>]\n' + \
                    '> `Спамит в канал.`\n> \n' + \
                    '> **Модификаторы:**\n' + \
                    '> `?digit`** - *цифра***\n' + \
                    '> `?letter`** - *латинская буква***\n' + \
                    '> `?prep`** - *знак препинания***\n' + \
                    '> `?char <мин.>, <макс>`** - *символ со случайным индексом***\n'

            elif command == 'ttsspam':
                resp = '> **ttsspam** [<***количество***> <***\\*текст***>]\n' + \
                    '> `Спамит в канал. (+TTS, требуются права отправки tts сообщений)`\n> \n' + \
                    '> **Модификаторы:**\n' + \
                    '> `?digit`** - *цифра***\n' + \
                    '> `?letter`** - *латинская буква***\n' + \
                    '> `?prep`** - *знак препинания***\n' + \
                    '> `?char <мин.>, <макс>`** - *символ со случайным индексом***\n> \n' + \
                    '> **? - При отправке TTS сообщения, оно будет воспроизведено у всех участников, которые находятся в канале.**'

            elif command == 'lag_spam':
                resp = '> **lag_spam** [<***тип лагов (ascii | chains)***> <***количество***>]\n' + \
                    '> `Запускает лаг-атаку на канал. У всех, кто будет находиться в канале, будет сильно лагать (тормозить).`\n> \n' + \
                    '> `chains`** - сообщения с эмодзи цепей (очень сильные лаги)**\n' + \
                    '> `ascii`** - сообщения со случайными символами (слабые лаги)**'

            elif command == 'stop_spam':
                resp = '> **stop_spam**\n' + \
                    '> `Останавливает все спам-атаки и лаг-атаки.`'

            elif command == 'masspin':
                resp = '> **masspin** [<***количество сообщений***>]\n' + \
                    '> `Массово закрепляет сообщения.`'

            elif command == 'calculate':
                resp = '> **calculate** [<***\\*математическое выражение***>\n' + \
                    '> `Вычисляет значение выражения.`'

            elif command == 'case_translate':
                resp = '> **case_translate** [<***\\*текст***>]\n' + \
                    '> `Переводит раскладку. (автоматическое обнаружение раскладки)`'

            elif command == 'translate':
                resp = '> **translate** [<***из языка***> <***в язык***> <***\\*текст***>]\n' + \
                    '> `Переводит язык.`'

            elif command == 'unspoiler':
                resp = '> **unspoiler** [<***ответ на сообщение***>]\n' + \
                    '> `Убирает все спойлеры с сообщения. (требуется ответ на сообщение, с которого нужно снять спойлеры)`'

            elif command == 'spoiler':
                resp = '> **spoiler** [<***\\*текст***>]\n' + \
                    '> `Создаёт сообщение с большим количеством спойлеров.`\n> \n' + \
                    '> `Обычный`** - по одному слову на спойлер**\n' + \
                    '> `С "1>" в начале`** - по одной букве на спойлер**'

            elif command == 'base64':
                resp = '> **base64** [<***режим (decode | encode)***> <***\\*текст***>]\n' + \
                    '> `Шифрует/расшифровывает base64 шифр.`'

            elif command == 'rand':
                resp = '> **rand** [<***мин.***> <***макс.***>]\n' + \
                    '> `Создаёт рандомное (случайное) число.`'

            elif command == 'tinyurl':
                resp = '> **tinyurl** [<***\\*оригинальная ссылка***>]\n' + \
                    '> `Укорачивает ссылку.`'

            elif command == 'color':
                resp = '> **color** [<***тег/название цвета***>]\n' + \
                    '> `Отображает цвет в виде картинки.`'

            elif command == 'read_all':
                resp = '> **read_all**\n' + \
                    '> `Помечает сообщения на всех серверах как прочитанные.`'

            elif command == 'reverse':
                resp = '> **reverse** [<***\\*текст***>]\n' + \
                    '> Переворачивает текст.`'

            elif command == 'user':
                resp = '> **user** [<***пользователь***>]\n' + \
                    '> `Получает данные о пользователе.`'

            elif command == 'guild':
                resp = '> **guild**\n' + \
                    '> `Получает данные о сервере. (в котором была выполнена команда)`'

            elif command == 'role':
                resp = '> **role [<***роль***>]**\n' + \
                    '> `Получает данные о роли.`'

            elif command == 'ping':
                resp = '> **ping**\n' + \
                    '> `Получает задержку от клиента (этого устройства) к серверам discord.`'

            elif command == 'del_channels':
                resp = '> **del_channels**\n' + \
                    '> `Удаляет все каналы на сервере. (требуются права управлять каналами)`'

            elif command == 'create_channels':
                resp = '> **create_channels** [<***\\*имя***>]\n' + \
                    '> `Создаёт 250 каналов на сервере. (требуются права управлять каналами)`'

            elif command == 'massban':
                resp = '> **massban**\n' + \
                    '> `Устраивает массовый бан. (требуются права банить участников)`'

            elif command == 'del_roles':
                resp = '> **del_roles**\n' + \
                    '> `Удаляет роли на сервере, которые ниже вашей. (требуются права управлять ролями)`'

            elif command == 'create_roles':
                resp = '> **create_roles** [<***\\*имя***>]\n' + \
                    '> `Создаёт 250 ролей на сервере. (требуются права управлять ролями)`'

            elif command == 'del_emojis':
                resp = '> **del_emojis**\n' + \
                    '> `Удаляет все эмодзи на сервере. (требуются права управлять эмодзи)`'

            elif command == 'del_invites':
                resp = '> **del_invites**\n' + \
                    '> `Удаляет все приглашения на сервере. (требуются права управлять сервером)`'

            elif command == 'webhook_spam':
                resp = '> **webhook_spam** [<***\\*текст***>]\n' + \
                    '> `Спамит вебхуками на всех каналах. (+TTS)`\n> \n' + \
                    '> **? - При отправке TTS сообщения, оно будет воспроизведено у всех участников, которые находятся в канале.**'

            elif command == 'nuke':
                resp = '> **nuke** [<***имена для каналов/ролей и т.д.***> <***\\*текст***>]\n' + \
                    '> `Устраивает полный беспредел на сервере. (требуются права администратора)`'

            elif command == 'auto_response':
                resp = '> **auto_response** [<***триггер***> <***\\*ответ***>]\n' + \
                    '> `Добавляет значение в автоответчик.`'

            elif command == 'del_auto_response':
                resp = '> **del_auto_response** [<***\\*триггер***>]\n' + \
                    '> `Удаляет значение из автоответчика.`'

            elif command == 'wipe_auto_response':
                resp = '> **wipe_auto_response**\n' + \
                    '> `Сбрасывает настройки автоответчика.`'

            elif command == 'animate':
                resp = '> **animate** [<***задержка, в секундах***> <***\\*статусы, по одному на строку***>]\n' + \
                    '> `Анимирует статус.`\n> \n' + \
                    '> **Иконки статусов:**\n' + \
                    '> ***online* - 🟢 `в сети`, *idle* - 🟡 `неактивен`, *dnd* - 🔴 `не беспокоить`, *invisible* - ⚪ `невидимка`**\n> \n' + \
                    '> `idle;;Hello`** - будет установлен статус "*Hello*" и иконка *🟡 неактивен*.**\n' + \
                    '> `idle`** - будет установлена иконка *🟡 неактивен*, статус изменён не будет.**\n' + \
                    '> `Hello`** - будет установлен статус "*Hello*", иконка изменена не будет.**\n> \n' + \
                    '> **Задержка:** `wait <задержка>`'

            elif command == 'stop_animate':
                resp = '> **stop_animate**\n' + \
                    '> `Останавливает анимацию статуса.`'

            elif command == 'copy_avatar':
                resp = '> **copy_avatar** [<***пользователь***>]\n' + \
                    '> `Копирует аватар у пользователя.`'

            elif command == 'copy_status':
                resp = '> **copy_status** [<***пользователь***>]\n' + \
                    '> `Копирует статус у пользователя.`'

            elif command == 'copy_guild_nick':
                resp = '> **copy_guild_nick** [<***пользователь***>]\n' + \
                    '> `Копирует имя пользователя на сервер.`'

            elif command == 'copy_all':
                resp = '> **copy_all** [<***пользователь***>]\n' + \
                    '> `Копирует аватарку, статус и имя у пользователя.`'

            elif command == 'ytcomment':
                resp = '> **ytcomment** [<***пользователь***> <***\\*текст***>]\n' + \
                    '> `Создаёт фейковые YouTube комментарии.`'

            elif command == 'tweet':
                resp = '> **tweet** [<***пользователь***> <***\\*текст***>]\n' + \
                    '> `Создаёт фейковые твиты (посты в Twitter).`'

            elif command == 'pixelate':
                resp = '> **pixelate** [<***пользователь***>]\n' + \
                    '> `Пикселизирует аватарку пользователя.`'

            elif command == 'blur':
                resp = '> **blur** [<***пользователь***>]\n' + \
                    '> `Размывает аватарку пользователя.`'

            elif command == 'stupid':
                resp = '> **stupid** [<***пользователь***> <***\\*текст***>]\n' + \
                    '> `Создаёт мем "Oh no its stupid".`'

            elif command == 'simpcard':
                resp = '> **simpcard** [<***пользователь***>]\n' + \
                    '> `Создаёт карточку для пользователя.`'

            elif command == 'horny':
                resp = '> **horny** [<***пользователь***>]\n' + \
                    '> `Создаёт лицензию для пользователя на ...`'

            elif command == 'lolice':
                resp = '> **lolice** [<***пользователь***>]\n' + \
                    '> `Лоли-полиция.`'

            elif command == 'lgbt':
                resp = '> **lgbt** [<***пользователь***>]\n' + \
                    '> `Круг ЛГБТ-цветов вокруг аватарки пользователя.`'

            elif command == 'pansexual':
                resp = '> **pansexual** [<***пользователь***>]\n' + \
                    '> `Круг цветов пансексуального флага вокруг аватарки пользователя.`'

            elif command == 'nonbinary':
                resp = '> **nonbinary** [<***пользователь***>]\n' + \
                    '> `Круг цветов небинарного флага вокруг аватарки пользователя.`'

            elif command == 'lesbian':
                resp = '> **lesbian** [<***пользователь***>]\n' + \
                    '> `Круг лесби-цветов вокруг аватарки пользователя.`'

            elif command == 'bi':
                resp = '> **bi** [<***пользователь***>]\n' + \
                    '> `Круг би-цветов вокруг аватарки пользователя.`'

            elif command == 'trans':
                resp = '> **trans** [<***пользователь***>]\n' + \
                    '> `Круг цветов транссексуального флага вокруг аватарки пользователя.`'

            elif command == 'gay':
                resp = '> **gay** [<***пользователь***>]\n' + \
                    '> `Гей-аватар пользователя.`'

            elif command == 'glass':
                resp = '> **glass** [<***пользователь***>]\n' + \
                    '> `Аватар пользователя, вид за стеклом.`'

            elif command == 'wasted':
                resp = '> **copy_all** [<***пользователь***>]\n' + \
                    '> `Аватар пользователя - потрачено (GTA).`'

            elif command == 'passed':
                resp = '> **passed** [<***пользователь***>]\n' + \
                    '> `Аватар пользователя - миссия пройдена (GTA).`'

            elif command == 'jail':
                resp = '> **jail** [<***пользователь***>]\n' + \
                    '> `Аватар пользователя за клеткой.`'

            elif command == 'communist':
                resp = '> **communist** [<***пользователь***>]\n' + \
                    '> `Аватар-коммунист пользователя.`'

            elif command == 'triggered':
                resp = '> **triggered** [<***пользователь***>]\n' + \
                    '> `Triggered-аватар пользователя.`'

            else:
                resp = f'> **Неизвестная команда - `{command}`. Введите `help` для получения полного списка команд.**'

        await ctx.send(resp)


def setup(bot):
    bot.add_cog(HelpCog(bot))

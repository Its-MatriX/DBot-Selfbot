from discord.ext import commands


class HelpCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help__(self, ctx, category=None, command_category=None):
        if ctx.author != self.bot.user:
            return

        if not category:
            resp = '⚒️ **Инструменты:** `help tools`\n' + \
                '👾 **Веселье:** `help fun`\n' + \
                '📕 **Информация:** `help info`\n' + \
                '🔥 **Краш:** `help nuke`\n' + \
                '🤖 **Авто-ответчик:** `help auto`\n' + \
                '🎞️ **Анимация статуса:** `help animation`'

        else:
            if category == 'fun':
                if not command_category:
                    resp = '🤬 **reaction_troll <*пользователь*> <*реакции*>:** `затроллить участника реакциями`\n' + \
                        '☠️ **repeat_troll <*пользователь*>:** `затроллить участника повторением его сообщений`\n' + \
                        '❌ **delete_troll <*пользователь*>:** `затроллить участника удалением его сообщений`\n' + \
                        '⛔ **untroll:** `остановить все троллинги`\n' + \
                        '🔮 **ball:** `магический шар`\n' + \
                        '⚙️ **reactions <*лимит сообщений*> <*реакция*>:** `поставить много реакций/остановить, если работает`'
                else:
                    if command_category == 'reaction_troll':
                        resp = '🤬 **reaction_troll:** `троллинг участника реакциями`\n' + \
                               '**При отправке сообщения, на сообщения участника будет ставиться реакция (можно несколько реакций).**'

                    elif command_category == 'repeat_troll':
                        resp = '☠️ **repeat_troll:** `троллинг участника повторением сообщений`\n' + \
                               '**Все сообщения, отправляемые указанным участником, будут повторяться.**'

                    elif command_category == 'delete_troll':
                        resp = '❌ **delete_troll:** `троллинг участника удалением сообщений`\n' + \
                               '**Все сообщения, отправляемые указанным участником, будут удаляться.**'

                    elif command_category == 'untroll':
                        resp = '⛔ **untroll:** `остановить троллинг`\n' + \
                               '**Троллинг будет остановлен.**'

                    elif command_category == 'reactions':
                        resp = '⚙️ **reaction:** `спам реакциями`\n' + \
                               '**На все сообщения в канале будут поставлены реакции.**'

                    elif command_category == 'ball':
                        resp = '🔮 **ball:** `магический шар`\n' + \
                               '**Магический шар, вы можете спросить у него, что угодно.**'

                    else:
                        resp = '❌ **Неверная категория, `reaction_troll`, `repeat_troll`, `delete_troll`, ' + \
                               '`untroll`, `reactions`**'

            elif category == 'tools':
                if not command_category:
                    resp = '🪄 **status <*параметры*> - `сменить статус`**\n' + \
                        '🗑️ **clear <*лимит истории сообщений*>:** `удалить свои сообщения`\n' + \
                        '🔥 **spam <*количество*> <*текст*>:** `спам-атака`\n' + \
                        '☠️ **lag_spam <*количество*> <*тип атаки*>:** `лаг-атака`\n' + \
                        '⛔ **stop_spam:** `остановить спам-атаку`\n' + \
                        '📌 **masspin <*количество*>:** `массовый закреп сообщений`\n' + \
                        '🧮 **calculate <*выражение*>:** `вычислить значение выражения`\n' + \
                        '⌨️ **case_translate <*текст*>:** `перевод раскладки`\n' + \
                        '🎈 **translate <*с языка*> <*в язык*> <*текст*>:** `перевод текста`\n' + \
                        '✍️ **unspoiler <*текст*>:** `снять все спойлеры`\n' + \
                        '🤬 **spoiler <*текст*>:** `заспойлерить текст (`1>"текст"`, если надо, чтобы спойлеры были по одному на букву.)`\n' + \
                        '🔗 **base64 <*режим*> <*текст*>:** `Шифрование base64 (d - расшифровать; e - зашифровать)`\n' + \
                        '🔢 **rand_number <*мин*> <*макс*>:** `Шифрование base64 (d - расшифровать; e - зашифровать)`\n'

                else:
                    if command_category == 'status':
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

                    elif category == 'clear':
                        resp = '🗑️ **clear <*лимит истории сообщений*>:** `удалить свои сообщения`\n' + \
                               '**Удаляет все сообщения от бота, которые были замечены в истории сообщений.**'

                    elif command_category == 'spam':
                        resp = '🔥 **spam <*количество*> <*текст/модификаторы*>:** `спам`\n' + \
                            '**Модификаторы:**\n' + \
                            '`?digit` - *цифра*\n' + \
                            '`?letter` - *латинская буква*\n' + \
                            '`?prep` - *знак препинания*\n' + \
                            '`?char <мин.>, <макс>` - *символ со случайным индексом*\n'

                    elif command_category == 'lag_spam':
                        resp = '☠️ **lag_spam:** `лаг-атака`\n' + \
                               '**Лаг-атака (вызывает жуткие лаги), варианты: `chains` - цепи, `ascii` - ascii символы.**'

                    elif category == 'stop_spam':
                        resp = '⛔ **stop_spam:** `остановить атаку`\n' + \
                               '**Останавливает все запущенные спам-атаки.**'

                    elif command_category == 'masspin':
                        resp = '📌 **masspin:** `массовый закреп сообщений`\n' + \
                               '**Массово закрепляет сообщения.**'

                    elif command_category == 'case_translate':
                        resp = '⌨️ **case_translate:** `перевод раскладки`\n' + \
                               '**Переводит раскладку (с русской на английскую, и наоборот, автоматическое распознавание раскладки).**'

                    elif command_category == 'calculate':
                        resp = '🧮 **calculate:** `вычислить значение выражения`\n' + \
                               '**Вычисляет значение выражения (переменная bot не разрешена, чтобы вы случайно не отправили свой токен).**'

                    elif command_category == 'translate':
                        resp = '🎈 **translate:** `перевод текста`\n' + \
                               '**Переводит текст с одного языка на другой.**'

                    elif command_category == 'unspoiler':
                        resp = '✍️ **unspoiler:** `снять все спойлеры`\n' + \
                               '**Снять все спойлеры с бесючего сообщения. (вы должны ответить на сообщение, где нужно снять спойлеры)**'

                    elif command_category == 'spoiler':
                        resp = '🤬 **spoiler <*текст*>:** `заспойлерить текст (`1>"текст"`, если надо, чтобы спойлеры были по одному на букву.)\n' + \
                               '**Создать сообщение с бесючими спойлерами.**'

                    elif command_category == 'base64':
                        resp = '🔗 **base64:** `Шифрование base64 (d - расшифровать; e - зашифровать)`\n' + \
                               '**Шифрование/расшифрование, используя base64.**'

                    else:
                        resp = '❌ **Неверная категория, `status`, `spam`, `lag_spam`, `stop_spam`, `masspin`, `case_translate`, `calculate`, `translate` ' + \
                            '`unspoiler`, `spoiler`**'

            elif category == 'info':
                if not command_category:
                    resp = '👤 **user <*пользователь*>:** `информация о пользователе`\n' + \
                        '👥 **guild:** `информация о сервере`\n' + \
                        '⌚ **ping:** `задержка бота`'

                else:
                    if command_category == 'user':
                        resp = '👤 **user <*пользователь*>:** `информация о пользователе`\n' + \
                               '**Получение данных о участнике сервера/глобальном пользователе.**'

                    elif command_category == 'guild':
                        resp = '👥 **guild:** `информация о сервере`\n' + \
                               '**Получение данных о сервере.**'

                    elif command_category == 'ping':
                        resp = '⌚ **ping:** `задержка бота`\n' + \
                               '**Получение задержки бота.**'

                    else:
                        resp = '❌ **Неверная категория, `user`, `guild`, `ping`**'

            elif category == 'nuke':
                if not command_category:
                    resp = '🗑️ **del_channels:** `удалить все каналы на сервере`\n' + \
                        '📨 **create_channels <*имя*>:** `создать много каналов`\n' + \
                        '☠️ **massban:** `массовый бан`\n' + \
                        '🗑️ **del_roles:** `удалить все роли на сервере`\n' + \
                        '🎭 **create_roles <*имя*>:** `создать много ролей`\n' + \
                        '🗑️ **del_emojis:** `удалить все эмодзи на сервере`\n' + \
                        '🗑️ **del_invites:** `удалить все приглашения на сервере`\n' + \
                        '🔥 **webhook_spam <*сообщение*>:** `создать много вебхуков, и спамить ими (+TTS)`\n' + \
                        '☠️ **nuke "<*имена для каналов/ролей*>" <*сообщение*>:** `полный краш`'

                else:
                    if command_category == 'del_channels':
                        resp = '🗑️ **del_channels:** `удалить все каналы на сервере`\n' + \
                               '**Удалить все каналы на сервере, который требуется крашнуть.**'

                    elif command_category == 'create_channels':
                        resp = '📨 **create_channels:** `создать много каналов`\n' + \
                               '**Создать 250 каналов на сервере.**'

                    elif command_category == 'massban':
                        resp = '☠️ **massban:** `массовый бан`\n' + \
                               '**Устроить массовый бан (Внимание! Клиент не видит всех участников сервера! Во время краша баньте участников вручную!).**'

                    elif command_category == 'del_roles':
                        resp = '🗑️ **del_roles:** `удалить все роли на сервере`\n' + \
                               '**Удалить все роли на сервере, который требуется крашнуть.**'

                    elif command_category == 'create_roles':
                        resp = '🎭 **create_roles:** `создать много ролей`\n' + \
                               '**Создать 250 ролей на сервере.**'

                    elif command_category == 'del_emojis':
                        resp = '🗑️ **del_emojis:** `удалить все эмодзи на сервере`\n' + \
                               '**Удалить все эмодзи на сервере, который требуется крашнуть.**'

                    elif command_category == 'del_invites':
                        resp = '🗑️ **del_invites:** `удалить все эмодзи на сервере`\n' + \
                               '**Удалить все приглашения на сервере, который требуется крашнуть.**'

                    elif command_category == 'webhook_spam':
                        resp = '🔥 **webhook_spam:** `создать много вебхуков, и спамить ими (+TTS)`\n' + \
                               '**Создать по одному вебхуку на канал, и спамить (+TTS: у всех участников будет воспроизводиться текст сообщения).**'

                    elif command_category == 'nuke':
                        resp = '☠️ **nuke:** `полный краш`\n' + \
                               '**Задействует все краш-команды, и полностью крашит сервер.**'

                    else:
                        resp = '❌ **Неверная категория, `del_channels`, `create_channels`, `massban`, `del_roles`, `create_roles`, `del_emojis` ' + \
                               '`del_invites`, `webhook_spam`, `nuke`**'

            elif category == 'auto':
                if not command_category:
                    resp = '➕ **auto_response "<*триггер*>" <*ответ*>:** `добавить значение в авто-ответчик`\n' + \
                        '❌ **del_auto_response "<*триггер*>":** `удалить значение из авто-ответчика`\n' + \
                        '🗑️ **wipe_auto_response:** `сбросить значения авто-ответчика`'

                else:
                    if command_category == 'auto_response':
                        resp = '➕ **auto_response "<*триггер*>" <*ответ*>:** `добавить значение в авто-ответчик`\n' + \
                               '**Добавляет значение в авто-ответчик.**'

                    elif command_category == 'del_auto_response':
                        resp = '❌ **del_auto_response "<*триггер*>":** `удалить значение из авто-ответчика`\n' + \
                               '**Удалить значение из авто-ответчика.**'

                    elif command_category == 'wipe_auto_response':
                        resp = '🗑️ **wipe_auto_response:** `сбросить значения авто-ответчика`\n' + \
                               '**Полностью сбросить все настройки авто-ответчика.**'

                    else:
                        resp = '❌ **Неверная категория, `auto_response`, `del_auto_response`, `wipe_auto_response`**'

            elif category == 'animation':
                if not command_category:
                    resp = '🎞️ **animate "<*задержка*>" <*статусы (разделять новой строкой)*>:** `запустить анимацию`\n' + \
                        '⛔ **stop_animate:** `остановить анимацию`\n' + \
                        '\n' + \
                        '`idle;;test` - **установить значок статуса "неактивен" + статус "test"**\n' + \
                        '`idle` - **установить значок статуса "неактивен", статус изменён не будет**\n' + \
                        '`test` - **статус "test", значок статуса изменён не будет**\n' + \
                        '\n' + \
                        '**Иконки статусов:**\n' + \
                        '🟢 `online` - *в сети*\n' + \
                        '🟡 `idle` - *неактивен*\n' + \
                        '🔴 `dnd` - *не беспокоить*\n' + \
                        '⚪ `invisible` - *невидимка*\n'

                else:
                    if command_category == 'animate':
                        resp = '🎞️ **animate "<*задержка*>" <*статусы (разделять новой строкой)*>:** `запустить анимацию`\n' + \
                               '**Анимация. Написание статусов, жеталельно, начинайте с новой строки, после основной команды.**'

                    elif command_category == 'stop_animate':
                        resp = '⛔ **stop_animate:** `остановить анимацию`\n' + \
                               '**Остановить выполнение анимации.**'

                    else:
                        resp = '❌ **Неверная категория, `animate`, `stop_animate`**'

            else:
                resp = '❌ **Неверная категория, `fun`, `help`, `info`, `nuke`, `auto`, `animation`**'

        await ctx.message.delete()
        await ctx.send(resp)


def setup(bot):
    bot.add_cog(HelpCog(bot))

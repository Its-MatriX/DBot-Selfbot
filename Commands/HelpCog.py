from discord.ext import commands


class helpCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help__(self, ctx, category=None, command_category=None):
        if ctx.author != self.bot.user:
            return

        if not category:
            resp =  '⚙️ **Инструменты:** `help tools`\n' + \
                    '🎃 **Веселье:** `help fun`\n'

        else:
            if category == 'fun':
                resp =  '🤬 **reaction_troll <*пользователь*> <*реакции*>:** `затроллить участника реакциями`\n' + \
                        '☠️ **repeat_troll <*пользователь*>:** `затроллить участника повторением его сообщений`\n' + \
                        '❌ **delete_troll <*пользователь*>:** `затроллить участника удалением его сообщений`\n' + \
                        '⛔ **untroll:** `остановить все троллинги`\n' + \
                        '⚙️ **reactions <*лимит сообщений*> <*реакция*>:** `поставить много реакций/остановить, если работает`'

            elif category == 'tools':
                if not command_category:
                    resp = '👤 **user <*пользователь*>:** `данные о пользователе`\n' + \
                        '🪄 **status <*параметры*> - `сменить статус`** '

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

                    else:
                        resp = '❌ **Неверная категория, `status`**'

            else:
                resp = '❌ **Неверная категория, `fun`, `help`**'

        await ctx.message.delete()
        await ctx.send(resp)


def setup(bot):
    bot.add_cog(helpCog(bot))
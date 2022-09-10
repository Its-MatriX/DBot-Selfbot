from discord import Status, Streaming, Game, Activity, ActivityType
from discord.ext import commands


class toolsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='user')
    async def user__(self, ctx, user):
        if ctx.author != self.bot.user:
            return

        in_guild = False

        user = user.replace('<@', '')
        user = user.replace('!', '')
        user = user.replace('>', '')
        user = int(user)
        user = await self.bot.fetch_user(
            user) if not ctx.guild else await ctx.guild.fetch_member(user)

        username = str(user)

        try:
            if user.guild:
                in_guild = True
                if user.status == Status.online:
                    status = 'В сети'

                if user.status == Status.idle:
                    status = 'Неактивен'

                if user.status == Status.dnd:
                    status = 'Не беспокоить'

                if user.status == Status.offline:
                    status = 'Неактивен'

                if user.is_on_mobile():
                    status += ' (телефон)'

                else:
                    status += ' (ПК)'

            try:
                is_owner = 'Да' if user.owner else 'Нет'
            except:
                is_owner = 'Нет'
            is_admin = 'Да' if user.guild_permissions.administrator else 'Нет'
        except:
            pass

        is_bot = 'Да' if user.bot else 'Нет'

        response = ''

        response += f'**Имя пользователя:** `{username}`\n'

        if in_guild:
            response += f'**Статус**: `{status}`\n'
            response += f'**Владелец**: `{is_owner}`\n'
            response += f'**Администратор**: `{is_admin}`\n'

        response += f'**Бот**: `{is_bot}`\n'

        response = response.replace('\n??delthis', '')

        await ctx.message.delete()
        await ctx.send(response)

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
            twitch_url = 'https://' + status[1] if 'https://' not in status[
                1] else status[1]
            stream_name = ' '.join(status[2:])

            await self.bot.change_presence(activity=Streaming(name=stream_name,
                                                              url=twitch_url),
                                           status=Status.online)
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


def setup(bot):
    bot.add_cog(toolsCog(bot))

from discord import Status, Member, http
from discord.ext import commands
import requests


class InfoCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='user')
    async def user__(self, ctx, user: Member = None):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if user == None:
            user = ctx.author

        if ctx.guild:
            user_fetched = ctx.guild.get_member(user.id)

        if ctx.guild:
            global_user = False
        else:
            global_user = True

        resp = ''

        url = 'http://tinyurl.com/api-create.php?url=' + str(user.avatar_url)
        avatar_url = requests.get(url).text

        if global_user:
            resp += f'> **Имя пользователя:** `{user}`\n'
            resp += f'> **ID:** `{user.id}`\n'
            resp += f'> **Бот:** `{"Да" if user.bot else "Нет"}`\n'
            resp += f'> **Друг:** `{"Да" if user.is_friend() else "Нет"}`\n'
            resp += f'> **Аватар:** **{avatar_url}**\n'
            created_at = round(user.created_at.timestamp())
            resp += f'> **Создано:** **<t:{created_at}:R>**'

            if user.premium_since:
                resp += f'\n> \n> ***Дополнительно (Nitro)***\n'
                premium_since = round(user.premium_since.timestamp())
                resp += f'> **Купил Nitro**: **<t:{premium_since}:R>**'

        else:
            resp += f'> **Имя пользователя:** `{user}`\n'
            resp += f'> **Имя на сервере:** `{user.display_name}`\n'
            resp += f'> **ID:** `{user.id}`\n'
            resp += f'> **Бот:** `{"Да" if user.bot else "Нет"}`\n'
            resp += f'> **Аватар:** **{avatar_url}**\n'
            created_at = round(user.created_at.timestamp())
            resp += f'> **Создано:** **<t:{created_at}:R>**\n'

            joined_at = round(user.joined_at.timestamp())
            resp += f'> **Присоединился:** **<t:{joined_at}:R>**\n'

            try:
                if user_fetched.status == Status.online:
                    status_icon = 'В сети'

                elif user_fetched.status == Status.idle:
                    status_icon = 'Неактивен'

                elif user_fetched.status == Status.dnd:
                    status_icon = 'Не беспокоить'

                elif user_fetched.status == Status.offline:
                    status_icon = 'Не в сети'

                if user_fetched.is_on_mobile():
                    status_icon += ' (телефон)'

                resp += f'> **Статус:** `{status_icon}`\n'
            except:
                resp += f'> **Статус:** `Не удалось определить`\n'

            resp += f'> **Высшая роль:** `{user.top_role.name}`\n'
            resp += f'> **Имеет ролей:** `{len(user.roles)}`\n'
            resp += f'> **Администратор:** `{"Да" if user.guild_permissions.administrator else "Нет"}`'

            if user.guild.owner:
                resp += f'> **Владелец:** `{"Да" if user.id == user.guild.owner.id else "Нет"}`'

            if user.premium_since:
                resp += f'\n> \n> ***Дополнительно (Nitro)***\n'
                premium_since = round(user.premium_since.timestamp())
                resp += f'> **Купил Nitro**: **<t:{premium_since}:R>**'

                user_http = await self.bot.http.request(
                    http.Route("GET", f"/users/{user.id}"))

                banner_id = user_http["banner"]

                if banner_id:
                    banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"

                    url = 'http://tinyurl.com/api-create.php?url=' + str(
                        banner_url)
                    banner_url = requests.get(url).text

                    resp += f'\n> **Баннер**: **{banner_url}**'

        await ctx.send(resp)

    @commands.command(name='guild')
    async def guild__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not ctx.guild:
            return

        resp = ''

        afk_channel = ctx.guild.afk_channel if ctx.guild.afk_channel else 'Нет'

        resp += f'> **Название:** `{ctx.guild.name}`\n'
        resp += f'> **ID:** `{ctx.guild.id}`\n'

        try:
            resp += f'> **AFK канал:** {afk_channel.mention}\n'
            resp += f'> **AFK таймаут:** `{ctx.guild.afk_timeout} секунд`\n'
        except:
            resp += f'> **AFK канал:** `Нет`\n'

        try:
            resp += f'> **Канал с правилами:** {ctx.guild.rules_channel.mention}\n'
        except:
            resp += f'> **Канал с правилами:** `Нет`\n'

        verification = str(ctx.guild.verification_level)

        if verification == 'none':
            verification = 'Отсутствует'
        elif verification == 'low':
            verification = 'Низкий'
        elif verification == 'medium':
            verification = 'Средний'
        elif verification == 'high':
            verification = 'Высокий'
        elif verification == 'extreme':
            verification = 'Самый высокий'

        resp += f'> **Уровень верификации:** `{verification}`\n'

        roles = len(ctx.guild.roles)
        admin_roles = len(
            [x for x in ctx.guild.roles if x.permissions.administrator])

        resp += f'> **Роли:** `{roles}, администраторских: {admin_roles}`\n'

        channels = len(ctx.guild.channels)
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        cateories = len(ctx.guild.categories)

        resp += f'> **Каналы:** `{channels} (текстовых: {text_channels}, голосовых: {voice_channels}, категорий: {cateories})`\n'

        resp += f'> **Описание:** `{ctx.guild.description}`\n'

        url = 'http://tinyurl.com/api-create.php?url=' + str(
            ctx.guild.icon_url)
        icon_url = requests.get(url).text

        resp += f'> **Иконка:** **{icon_url}**\n'

        try:
            url = 'http://tinyurl.com/api-create.php?url=' + str(
                ctx.guild.banner.url)
            banner_url = requests.get(url).text
            resp += f'> **Баннер:** **{banner_url}**\n'
        except:
            pass

        url = 'http://tinyurl.com/api-create.php?url=' + f'https://discord.com/widget?id={ctx.guild.id}'
        widget_url = requests.get(url).text

        resp += f'> **Виджет:** **{widget_url}**\n'

        await ctx.send(resp)

    @commands.command(name='ping')
    async def ping__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        ping = round(self.bot.latency * 1000)

        resp = f'> **Пинг:** `{ping} МС`'
        await ctx.send(resp)


def setup(bot):
    bot.add_cog(InfoCog(bot))

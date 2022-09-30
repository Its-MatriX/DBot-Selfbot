from discord.ext import commands
from discord import Member
from datetime import datetime, timedelta
import requests
from urllib.parse import quote


def send_request(bot, method, path, json, add_headers):
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Origin': 'https://discord.com',
        'Pragma': 'no-cache',
        'Referer': 'https://discord.com/channels/@me',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': bot.http.user_agent,
        'X-Super-Properties': bot.http.encoded_super_properties,
        'Authorization': bot.http.token
    }

    for key in list(add_headers.keys()):
        headers[key] = add_headers[key]

    if method == 'GET':
        response = requests.get('https://discord.com/api/v7' + path,
                                headers=headers,
                                json=json)

    elif method == 'POST':
        response = requests.post('https://discord.com/api/v7' + path,
                                 headers=headers,
                                 json=json)

    elif method == 'PATCH':
        response = requests.patch('https://discord.com/api/v7' + path,
                                  headers=headers,
                                  json=json)

    elif method == 'PUT':
        response = requests.put('https://discord.com/api/v7' + path,
                                headers=headers,
                                json=json)

    elif method == 'HEAD':
        response = requests.head('https://discord.com/api/v7' + path,
                                 headers=headers,
                                 json=json)

    elif method == 'DELETE':
        response = requests.delete('https://discord.com/api/v7' + path,
                                   headers=headers,
                                   json=json)

    return response


class ModerationCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='mute')
    async def mute__(self,
                     ctx,
                     member: Member,
                     duration: str,
                     *,
                     reason='Причина не указана'):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        duration = duration.strip()

        try:
            if duration.endswith('с') or duration.endswith('s'):
                duration_integer = int(duration[:-1:1])

            elif duration.endswith('м') or duration.endswith('m'):
                duration_integer = int(duration[:-1:1]) * 60

            elif duration.endswith('ч') or duration.endswith('h'):
                duration_integer = int(duration[:-1:1]) * 3600

            elif duration.endswith('д') or duration.endswith('d'):
                duration_integer = int(duration[:-1:1]) * 86400

            else:
                raise NameError

        except:
            await ctx.send(
                '**❌ Неправильно указана длительность мьюта. Введите `help mute` для инструкции.**'
            )

            return

        if duration_integer > 86400 * 28:
            await ctx.send(
                f'> **❌ Мьют - ошибка**\n> \n> Длительность мьюта не должна превышать **28** дней.'
            )

            return

        timeout = (datetime.utcnow() +
                   timedelta(seconds=duration_integer)).isoformat()
        json = {"communication_disabled_until": timeout}

        reason_quoted = quote(reason)

        response = send_request(self.bot, 'PATCH',
                                f'/guilds/{ctx.guild.id}/members/{member.id}',
                                json, {'X-Audit-Log-Reason': reason_quoted})

        if response.ok:
            await ctx.send(
                f'> **🔇 Мьют**\n> \n> **{member.mention}** получает мьют!\n> Длительность: **{duration}**\n> Причина: **{reason}**'
            )

        else:
            if 'missing permissions' in response.text.lower():
                await ctx.send(
                    f'> **❌ Мьют - ошибка**\n> \n> Недостаточно прав для мьюта **{member}**'
                )

                return

            else:
                await ctx.send(
                    f'> **❌ Мьют - ошибка**\n> \n> Произошла ошибка при попытке мьюта **{member}**'
                )

                return

    @commands.command(name='unmute')
    async def unmute__(self,
                       ctx,
                       member: Member,
                       *,
                       reason='Причина не указана'):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        json = {"communication_disabled_until": 0}

        reason_quoted = quote(reason)

        response = send_request(self.bot, 'PATCH',
                                f'/guilds/{ctx.guild.id}/members/{member.id}',
                                json, {'X-Audit-Log-Reason': reason_quoted})

        if response.ok:
            await ctx.send(
                f'> **🔊 Размьют**\n> \n> С **{member.mention}** снят мьют!\n> \n> Причина: **{reason}**'
            )
            return

        else:
            if 'missing permissions' in response.text.lower():
                await ctx.send(
                    f'> **❌ Размьют - ошибка**\n> \n> Недостаточно прав для размьюта **{member}**'
                )

                return

            else:
                await ctx.send(
                    f'> **❌ Размьют - ошибка**\n> \n> Произошла ошибка при попытке мьюта **{member}**'
                )

                return

    @commands.command(name='ban')
    async def ban__(self, ctx, user: str, *, reason='Причина не указана'):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if user.isdigit():
            user = await self.bot.fetch_user(int(user))

        else:
            if user.replace('<@', '').replace('!', '').replace('>',
                                                               '').isdigit():
                user = int(
                    user.replace('<@', '').replace('!', '').replace('>', ''))
                user = await self.bot.fetch_user(user)

            else:
                await ctx.send(
                    f'> **❌ Бан - ошибка**\n> \n> Укажите тег **{user}**, чтоба найти его среди прочих **{user}**.'
                )

                return

        try:
            await ctx.guild.ban(user, reason=reason)
            await ctx.send(
                f'> **☠️ Бан**\n> \n> **{user}** успешно забанен!\n> Причина: **{reason}**'
            )

        except Exception as e:
            if 'missing permissions' in str(e).lower():
                await ctx.send(
                    f'> **❌ Бан - ошибка**\n> \n> Недостаточно прав для бана участника **{user}**.'
                )

                return

            else:
                await ctx.send(
                    f'> **❌ Бан - ошибка**\n> \n> Произошла ошибка при попытке бана **{user}**'
                )

                return

    @commands.command(name='unban')
    async def unban__(self, ctx, *, user: str):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        is_id = False

        if '#' not in user:
            if user.isdigit():
                is_id = True

            else:
                await ctx.send(
                    f'> **❌ Разбан - ошибка**\n> \n> Укажите тег **{user}**, чтоба найти его среди прочих **{user}**.'
                )

                return

        if is_id:
            user = await self.bot.fetch_user(int(user))

            if not user:
                await ctx.send(
                    f'> **❌ Разбан - ошибка**\n> \n> Пользователь с ID **{user}** не найден.'
                )

                return

            try:
                await ctx.guild.unban(user)
                await ctx.send(
                    f'> **🎉 Разбан**\n> \n> **{user}** успешно разбанен!')
                return

            except Exception as e:
                if 'missing permissions' in str(e).lower():
                    await ctx.send(
                        f'> **❌ Разбан - ошибка**\n> \n> Недостаточно прав для разбана участников.'
                    )
                    return

                else:
                    await ctx.send(
                        f'> **❌ Разбан - ошибка**\n> \n> Произошла ошибка при попытке разбана **{user}**'
                    )

                    return

        else:
            bans = await ctx.guild.bans()

            for entry in bans:
                banned_user = entry.user

                if str(banned_user) == user:
                    try:
                        await ctx.guild.unban(banned_user)
                        await ctx.send(
                            f'> **🎉 Разбан**\n> \n> **{user}** успешно разбанен!'
                        )
                        return

                    except Exception as e:
                        if 'missing permissions' in str(e).lower():
                            await ctx.send(
                                f'> **❌ Разбан - ошибка**\n> \n> Недостаточно прав для разбана участников.'
                            )

                            return

                        else:
                            await ctx.send(
                                f'> **❌ Разбан - ошибка**\n> \n> Произошла ошибка при попытке разбана **{user}**'
                            )

                            return

    @commands.command(name='kick')
    async def kick(self, ctx, member: Member, *, reason):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        try:
            await member.kick(reason=reason)
            await ctx.send(
                f'> **🧹 Кик**\n> \n> **{member.mention}** успешно кикнут!')

        except Exception as e:
            if 'missing permissions' in str(e).lower():
                await ctx.send(
                    f'> **❌ Кик - ошибка**\n> \n> Недостаточно прав для кика участника **{member}**.'
                )

                return

            else:
                await ctx.send(
                    f'> **❌ Кик - ошибка**\n> \n> Произошла ошибка при попытке кика **{member}**'
                )

                return

    @commands.command(name='slowmode')
    async def slowmode__(self, ctx, duration: str):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        try:
            if duration.endswith('с') or duration.endswith('s'):
                duration_integer = int(duration[:-1:1])

            elif duration.endswith('м') or duration.endswith('m'):
                duration_integer = int(duration[:-1:1]) * 60

            elif duration.endswith('ч') or duration.endswith('h'):
                duration_integer = int(duration[:-1:1]) * 3600

            else:
                raise NameError

        except:
            await ctx.send(
                '**❌ Неправильно указана длительность медленного режима. Введите `help slowmode` для инструкции.**'
            )

            return

        if duration_integer > 21600:
            await ctx.send(
                f'> **❌ Медленный режим - ошибка**\n> \n> Длительность медленного режима не должна превышать **6** часов.'
            )

            return

        try:
            await ctx.channel.edit(slowmode_delay=duration_integer)
            await ctx.send(
                f'> **⌛ Медленный режим**\n> \n> Установлен медленный режим: **{duration}**.'
            )

        except Exception as e:
            if 'missing permissions' in str(e).lower():
                await ctx.send(
                    f'> **❌ Медленный режим - ошибка**\n> \n> Недостаточно прав для установки медленного режима.'
                )

                return

            else:
                await ctx.send(
                    f'> **❌ Медленный режим - ошибка**\n> \n> Произошла ошибка при установке медленного режима.'
                )

                return


def setup(bot):
    bot.add_cog(ModerationCog(bot))

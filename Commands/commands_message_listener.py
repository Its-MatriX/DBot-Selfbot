from discord import Embed, RequestsWebhookAdapter, Webhook, DMChannel, GroupChannel
from discord.ext import commands
from re import findall
from Functions.discord_requests import send_request
from Functions.logger import log, log_error


class MessageListenerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        if bot.config['LOG_DELETES'] or bot.config['LOG_EDITS']:
            self.log_webhook = Webhook.from_url(
                bot.config['LOG_WEBHOOK'], adapter=RequestsWebhookAdapter())

        self.log_deletes = bot.config['LOG_DELETES']
        self.log_edits = bot.config['LOG_EDITS']

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if self.bot.user.id == message.author.id:
            return

        if self.log_deletes:
            if not isinstance(message.channel, [GroupChannel, DMChannel]):
                embed = Embed(title='Сообщение удалено', color=0xFF0000)

                resp = f'**Автор:** {message.author.mention} `({message.author.id})`\n' + \
                    f'**Канал:** {message.channel.mention} `({message.channel.id})`\n' + \
                    f'**Сервер:** `{message.guild.name} ({message.guild.id})`'

                embed.description = resp

                if message.content != '':
                    embed.add_field(name='Контент:',
                                    value=message.content,
                                    inline=False)

                attach_resp = ''
                attach_id = 1

                for attachment in message.attachments:
                    attach_resp += f'[№{attach_id}]({attachment.url}) '
                    attach_id += 1

                if attach_resp != '':
                    embed.add_field(name='Вложения:',
                                    value=attach_resp,
                                    inline=False)

                try:
                    self.log_webhook.send(embed=embed)
                except Exception as e:
                    log_error(f'Ошибка логгера сообщений: {e}')

            elif isinstance(message.channel, GroupChannel):
                embed = Embed(title='Сообщение удалено', color=0xFF0000)

                resp = f'**Автор:** {message.author.mention} `({message.author.id})`\n' + \
                    f'**Канал:** {message.channel.mention} `({message.channel.id}, группа)`\n'

                embed.description = resp

                if message.content != '':
                    embed.add_field(name='Контент:',
                                    value=message.content,
                                    inline=False)

                attach_resp = ''
                attach_id = 1

                for attachment in message.attachments:
                    attach_resp += f'[№{attach_id}]({attachment.url}) '
                    attach_id += 1

                if attach_resp != '':
                    embed.add_field(name='Вложения:',
                                    value=attach_resp,
                                    inline=False)

                try:
                    self.log_webhook.send(embed=embed)
                except Exception as e:
                    log_error(f'Ошибка логгера сообщений: {e}')

            elif isinstance(message.channel, DMChannel):
                embed = Embed(title='Сообщение удалено', color=0xFF0000)

                resp = f'**Автор:** {message.author.mention} `({message.author.id}, личные сообщения)`'

                embed.description = resp

                if message.content != '':
                    embed.add_field(name='Контент:',
                                    value=message.content,
                                    inline=False)

                attach_resp = ''
                attach_id = 1

                for attachment in message.attachments:
                    attach_resp += f'[№{attach_id}]({attachment.url}) '
                    attach_id += 1

                if attach_resp != '':
                    embed.add_field(name='Вложения:',
                                    value=attach_resp,
                                    inline=False)

                try:
                    self.log_webhook.send(embed=embed)
                except Exception as e:
                    log_error(f'Ошибка логгера сообщений: {e}')

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if self.bot.user.id == after.author.id:
            return

        if self.log_edits:
            if not isinstance(after.channel, [GroupChannel, DMChannel]):
                embed_about = Embed(title='Сообщение изменено', color=0xFFFF00)

                resp = f'**Автор:** {after.author.mention} `({after.author.id})`\n' + \
                    f'**Канал:** {after.channel.mention} `({after.channel.id})`\n' + \
                    f'**Сервер:** `{after.guild.name} ({after.guild.id})`'

                embed_about.description = resp

                attach_resp = ''
                attach_id = 1

                for attachment in before.attachments:
                    attach_resp += f'[№{attach_id}]({attachment.url}) '
                    attach_id += 1

                if attach_resp != '':
                    embed_about.add_field(name='Вложения:',
                                          value=attach_resp,
                                          inline=False)

                embed_before = Embed(title='До:',
                                     description=before.content,
                                     color=0x2ECC70)

                embed_after = Embed(title='После:',
                                    description=after.content,
                                    color=0x2ECCBE)

                try:
                    self.log_webhook.send(
                        embeds=[embed_about, embed_before, embed_after])
                except Exception as e:
                    log_error(f'Ошибка логгера сообщений: {e}')

            elif isinstance(after.channel, GroupChannel):
                embed_about = Embed(title='Сообщение изменено', color=0xFFFF00)

                resp = f'**Автор:** {after.author.mention} `({after.author.id})`\n' + \
                    f'**Канал:** {after.channel} `({after.channel.id}, группа)`'

                embed_about.description = resp

                attach_resp = ''
                attach_id = 1

                for attachment in before.attachments:
                    attach_resp += f'[№{attach_id}]({attachment.url}) '
                    attach_id += 1

                if attach_resp != '':
                    embed_about.add_field(name='Вложения:',
                                          value=attach_resp,
                                          inline=False)

                embed_before = Embed(title='До:',
                                     description=before.content,
                                     color=0x2ECC70)

                embed_after = Embed(title='После:',
                                    description=after.content,
                                    color=0x2ECCBE)

                try:
                    self.log_webhook.send(
                        embeds=[embed_about, embed_before, embed_after])
                except Exception as e:
                    log_error(f'Ошибка логгера сообщений: {e}')

            elif isinstance(after.channel, DMChannel):
                embed_about = Embed(title='Сообщение изменено', color=0xFFFF00)

                resp = f'**Автор:** {after.author.mention} `({after.author.id}, личные сообщения)`'

                embed_about.description = resp

                attach_resp = ''
                attach_id = 1

                for attachment in before.attachments:
                    attach_resp += f'[№{attach_id}]({attachment.url}) '
                    attach_id += 1

                if attach_resp != '':
                    embed_about.add_field(name='Вложения:',
                                          value=attach_resp,
                                          inline=False)

                embed_before = Embed(title='До:',
                                     description=before.content,
                                     color=0x2ECC70)

                embed_after = Embed(title='После:',
                                    description=after.content,
                                    color=0x2ECCBE)

                try:
                    self.log_webhook.send(
                        embeds=[embed_about, embed_before, embed_after])
                except Exception as e:
                    log_error(f'Ошибка логгера сообщений: {e}')

    @commands.Cog.listener()
    async def on_message(self, message):
        if 'discord.gift' in message.content:
            if self.bot.config['SNIPE_NITRO']:
                nitro_urls = findall('discord\.gift/[a-zA-Z1-9]*',
                                     message.content)

                for nitro_url in nitro_urls:
                    nitro_code = nitro_url.replace('discord.gift/', '')

                    response = send_request(
                        self.bot, 'POST',
                        f'/entitlements/gift-codes/{nitro_code}/redeem')

                    if response.ok:
                        log(f'Поздравляем! Вы успешно забрали Nitro от {message.author}!'
                            )

                    else:
                        if response.json(
                        )['message'] == 'Cannot redeem this gift in your location.':
                            log_error(
                                f'Не удалось забрать Nitro от {message.author}: '
                                + 'Не удаётся забрать Nitro в вашей стране.')

                        else:
                            log_error(
                                f'Не удалось забрать Nitro от {message.author}: '
                                +
                                'Неверный код (неверная ссылка, или кто-то другой уже забрал).'
                            )


def setup(bot):
    bot.add_cog(MessageListenerCog(bot))

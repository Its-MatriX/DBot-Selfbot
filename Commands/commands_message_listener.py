from colorama import Fore
from discord import Embed, RequestsWebhookAdapter, Webhook
from discord.ext import commands


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

            self.log_webhook.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if self.bot.user.id == after.author.id:
            return

        if self.log_edits:
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

            self.log_webhook.send(
                embeds=[embed_about, embed_before, embed_after])


def setup(bot):
    bot.add_cog(MessageListenerCog(bot))

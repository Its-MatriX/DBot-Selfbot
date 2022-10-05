from threading import Thread
from time import sleep

from discord.ext import commands
from Functions.discord_requests import send_request


class AnimatorState:
    is_working = False
    animation = None


class MainBot:
    bot = None


def set_custom_status(status_text=None, status_icon=None):
    if status_text:
        if status_icon:
            body = {
                'custom_status': {
                    'text': status_text
                },
                'status': status_icon
            }
        else:
            body = {'custom_status': {'text': status_text}}
    else:
        if status_icon:
            body = {'status': status_icon}
        else:
            return None

    resp = send_request(MainBot.bot, 'PATCH', '/users/@me/settings', body)

    return resp.status_code


def animate(delay, statuses):
    while AnimatorState.is_working:
        for status in statuses:
            if not AnimatorState.is_working:
                return

            if status.lower().startswith('wait'):
                wait = status.replace(' ', '').replace('wait', '')
                try:
                    sleep(float(wait))
                    continue
                except Exception:
                    pass

            status_icon = None
            status_text = None
            if status.lower() in ['online', 'idle', 'dnd', 'invisible']:
                status_icon = status.lower()
            else:
                if ';;' in status:
                    status = status.split(';;', 1)
                    if status[0].lower() in [
                            'online', 'idle', 'dnd', 'invisible'
                    ]:
                        status_icon = status[0].lower()
                        status_text = status[1]
                    else:
                        status_text = status[0] + ';;' + status[1]
                else:
                    status_text = status

            Thread(target=lambda: set_custom_status(status_text, status_icon)
                   ).start()
            sleep(delay)


class AnimationCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        MainBot.bot = bot

    @commands.command(name='animate')
    async def animate__(self, ctx, delay: float, *, animation: str):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        if not animation:
            return

        if AnimatorState.is_working:
            return

        if delay < 0.01 or delay > 3600:
            return

        if '\n' not in animation:
            return

        AnimatorState.is_working = True

        animation = animation.split('\n')
        Thread(target=lambda: animate(delay, animation)).start()

    @commands.command(name='stop_animate')
    async def stop_animate__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        AnimatorState.is_working = False


def setup(bot):
    bot.add_cog(AnimationCog(bot))

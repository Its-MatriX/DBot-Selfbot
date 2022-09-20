from threading import Thread
from time import sleep

import requests
from colorama import Fore
from discord.ext import commands


class AnimatorState:
    is_working = False
    animation = None


def set_custom_status(token, status_text=None, status_icon=None):
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

    headers = {'Authorization': token}

    resp = requests.patch('https://discord.com/api/v9/users/@me/settings',
                          json=body,
                          headers=headers)

    return resp.status_code


def animate(delay, token, statuses, show_logs):
    if show_logs:
        print(Fore.GREEN + 'Анимация статуса: ' + Fore.CYAN +
              f'Поток анимации запущен')

    while AnimatorState.is_working:
        for status in statuses:
            if not AnimatorState.is_working:
                return
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

            Thread(target=lambda: set_custom_status(token, status_text,
                                                    status_icon)).start()
            sleep(delay)


class AnimationCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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
        Thread(target=lambda: animate(delay, self.bot.http.token, animation,
                                      self.bot.show_logs)).start()

    @commands.command(name='stop_animate')
    async def stop_animate__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        AnimatorState.is_working = False


def setup(bot):
    bot.add_cog(AnimationCog(bot))

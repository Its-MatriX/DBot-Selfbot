from discord.ext import commands
from colorama import Fore
from time import sleep
from threading import Thread
import requests


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

    resp = requests.patch(
        'https://discord.com/api/v9/users/@me/settings',
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

            Thread(target=lambda: set_custom_status(token, status_text, status_icon
                                                    )).start()
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
            if self.bot.show_logs:
                print(Fore.GREEN + 'Анимация статуса: ' + Fore.CYAN +
                      f'Ошибка: animation: не задано')
            return

        if AnimatorState.is_working:
            if self.bot.show_logs:
                print(Fore.GREEN + 'Анимация статуса: ' + Fore.CYAN +
                      f'Ошибка: Анимация и так работает, чтобы остановить - stop_animate')
            return

        if delay < 0.01 or delay > 3600:
            if self.bot.show_logs:
                print(Fore.GREEN + 'Анимация статуса: ' + Fore.CYAN +
                      f'Ошибка: Задержка должна быть между 0.01 и 3600 (в секундах)')
            return

        if '\n' not in animation:
            if self.bot.show_logs:
                print(Fore.GREEN + 'Анимация статуса: ' + Fore.CYAN +
                      f'Ошибка: Требуется как минимум 2 строки')
            return

        AnimatorState.is_working = True

        if self.bot.show_logs:
            print(Fore.GREEN + 'Анимация статуса: ' + Fore.CYAN +
                  f'Запуск потока')

        animation = animation.split('\n')
        Thread(target=lambda: animate(delay, self.bot.http.token,
               animation, self.bot.show_logs)).start()

    @commands.command(name='stop_animate')
    async def stop_animate__(self, ctx):
        if ctx.author != self.bot.user:
            return

        await ctx.message.delete()

        AnimatorState.is_working = False

        if self.bot.show_logs:
            print(Fore.GREEN + 'Анимация статусы: ' + Fore.CYAN +
                  f'Остановка')


def setup(bot):
    bot.add_cog(AnimationCog(bot))

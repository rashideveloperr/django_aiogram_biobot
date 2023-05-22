import logging

from aiogram import Dispatcher
from aiogram.types import BotCommand
from aiogram.utils import executor
from django.core.management.base import BaseCommand

from aiobot.robot.config import dp


# from root.settings import WEBHOOK_URL


class Command(BaseCommand):
    help = 'Setting webhook'

    @staticmethod
    async def on_start(dis: Dispatcher):
        bot_commands = [
            BotCommand('start', 'Start'),
            BotCommand('utm', 'UTM')
        ]
        await dis.bot.set_my_commands(bot_commands)

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        executor.start_polling(dp, on_startup=self.on_start, skip_updates=True)

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ParseMode
from aiogram.utils.markdown import bold, escape_md
from django.utils.translation import gettext as _

from aiobot.robot.config import dp
from aiobot.robot.handlers.users.register.language import language

from ...validators import activate_user_language
from .menu import prepare_menu


@dp.message_handler(commands=['start'])
@activate_user_language
async def send_welcome(msg: Message, state: FSMContext, user, **kwargs):
    caption = bold("BioGroup") + escape_md(_('About BioGroup'))
    await msg.answer_photo('https://telegra.ph/file/346ffe2a83f93d04ced7e.png', caption, ParseMode.MARKDOWN_V2)
    if user.is_lead:
        await language(msg, state)
    else:
        await prepare_menu(msg)


@dp.message_handler(commands=['UTM'])
@activate_user_language
async def send_welcome(msg: Message, state: FSMContext, user, **kwargs):
    caption = bold("BioGroup") + escape_md(_('About BioGroup'))
    await msg.answer_photo('https://telegra.ph/file/346ffe2a83f93d04ced7e.png', caption, ParseMode.MARKDOWN_V2)
    if user.is_lead:
        await language(msg, state)
    else:
        await prepare_menu(msg)

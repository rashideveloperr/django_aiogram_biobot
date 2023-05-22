from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)
from django.utils.translation import activate
from django.utils.translation import gettext as _

from aiobot.models import TGUser
from aiobot.robot.config import dp
from aiobot.robot.handlers.users.menu import prepare_menu
from aiobot.robot.validators import activate_user_language


@dp.message_handler(Text('Язык/Til'))
@activate_user_language
async def language(msg: Message, state: FSMContext, **kwargs):
    languages = TGUser.Language.choices
    buttons = [InlineKeyboardButton(t, callback_data=c) for c, t in languages]
    keyboards = InlineKeyboardMarkup(1).add(*buttons)
    await msg.answer(_('Choose language'), reply_markup=keyboards)
    await state.set_state('lang_select')


@dp.callback_query_handler(state='lang_select')
@activate_user_language
async def language_select(callback: CallbackQuery, state: FSMContext, user: TGUser, **kwargs):
    data = callback.data
    user.lang = data
    await user.async_save()
    reply_markup = callback.message.reply_markup
    for key in reply_markup.inline_keyboard:
        if key[0].callback_data == data:
            key[0].text += ' ✅'
    await callback.message.edit_reply_markup(reply_markup)
    activate(data)
    if not user.is_lead:
        await prepare_menu(callback.message)
        await state.finish()
        return
    text = _('Input name')
    keyboard = ReplyKeyboardMarkup([[KeyboardButton(callback.from_user.full_name)]], True)
    await callback.message.answer(text, reply_markup=keyboard)
    await state.set_state('asking_for_name')

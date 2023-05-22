from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, KeyboardButton, Message, ReplyKeyboardMarkup
from django.utils.translation import gettext as _

from aiobot.models import TGUser
from aiobot.robot.config import dp
from aiobot.robot.handlers.users.menu import prepare_menu
from aiobot.robot.validators import activate_user_language


@dp.message_handler(state='asking_for_name', content_types=ContentType.TEXT)
@activate_user_language
async def getting_name(msg: Message, state: FSMContext, user: TGUser, **kwargs):
    text = _('Getting phone number')
    keyboard = ReplyKeyboardMarkup([[KeyboardButton(_('share phone number'), request_contact=True)]], True)
    await msg.answer(text, reply_markup=keyboard)
    user.fullname = msg.text
    await user.async_save()
    await state.set_state('asking_for_phone')


@dp.message_handler(state='asking_for_phone', content_types=ContentType.CONTACT)
@activate_user_language
async def getting_phone(msg: Message, state: FSMContext, user: TGUser, **kwargs):
    phone_number = msg.contact.phone_number
    user.phone_number = phone_number
    user.is_lead = False
    await user.async_save()
    await state.finish()
    await prepare_menu(msg)

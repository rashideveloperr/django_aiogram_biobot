from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup
from django.utils.translation import gettext as _

from ...config import dp
from ...validators import activate_user_language, is_msg_equal


async def prepare_menu(msg: Message, **kwargs):
    keyboards = ReplyKeyboardMarkup([
        [KeyboardButton(_('Products'))],
        [KeyboardButton(_('Feedback')), KeyboardButton('Язык/Til')],
    ], True)
    await msg.answer(_('Menu'), reply_markup=keyboards)


@dp.message_handler(lambda msg: is_msg_equal(msg, 'Feedback'))
@activate_user_language
async def get_feedback(msg: Message, **kwargs):
    text = _('Feedback Message')
    await msg.answer(text)

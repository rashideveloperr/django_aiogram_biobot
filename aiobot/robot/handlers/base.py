from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from django.utils.translation import gettext as _

from aiobot.robot.config import dp
from aiobot.robot.validators import activate_user_language


@dp.callback_query_handler(Text('cancel'), state='*')
@activate_user_language
async def cancel_state(callback: CallbackQuery, state: FSMContext, **kwargs):
    await state.finish()
    await callback.answer(_('Operation cancelled'), True)
    await callback.message.delete()

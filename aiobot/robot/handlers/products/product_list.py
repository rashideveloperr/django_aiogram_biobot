from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from django.utils.translation import gettext as _

from aiobot.models import Product, TGUser
from aiobot.robot.config import dp
from aiobot.robot.validators import activate_user_language, is_msg_equal


@dp.message_handler(lambda msg: is_msg_equal(msg, 'Products'))
@activate_user_language
async def show_product_list(msg: Message, user: TGUser, **kwargs):
    keyboards = [
        InlineKeyboardButton(await product.td_name(user.lang), callback_data=f'product_{product.id}')
        async for product in Product.objects.all()
    ]
    inline_mk = InlineKeyboardMarkup(2).add(*keyboards)
    caption = _('Products')
    await msg.answer_photo('https://telegra.ph/file/346ffe2a83f93d04ced7e.png', caption, reply_markup=inline_mk)

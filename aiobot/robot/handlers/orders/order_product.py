from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ParseMode,
)
from aiogram.utils.markdown import bold, code, escape_md, spoiler
from django.utils.translation import gettext as _
from root.settings import TELEGRAM_ADMINS

from aiobot.models import Order, Product, TGUser
from aiobot.robot.config import dp
from aiobot.robot.validators import activate_user_language


async def send_order_to_admins(msg: Message, order: Order, user: TGUser):
    product = await Product.objects.aget(id=order.product_id)
    temp = [
        "Обратная связь",
        f"Hомер заказа \-\- {order.pk}",
        f"Код товара \-\- {order.product_id}",
        f"Hазвание товара \-\- {escape_md(await product.td_name())}",
        '\n\-\-\-\n' + spoiler(escape_md(order.pass_message)) + '\n\-\-\-\n',
        bold('Имя - ') + code(user.fullname),
        bold('Юзер - ') + msg.from_user.mention,
        bold('Телефон - ') + code(user.phone_number),
        code(msg.from_user.id)
    ]
    text = '\n'.join(temp)
    for admin in TELEGRAM_ADMINS:
        await msg.bot.send_message(admin, text, ParseMode.MARKDOWN_V2)


@dp.callback_query_handler(Text(startswith='order_'))
@activate_user_language
async def order_products(callback: CallbackQuery, state: FSMContext, **kwargs):
    cancel = InlineKeyboardMarkup().add(InlineKeyboardButton(_('Cancel'), callback_data='cancel'))
    await callback.message.answer(_('Order Message'), reply_markup=cancel)
    await state.set_data({'product_id': int(callback.data[6:])})
    await state.set_state('order')


@dp.message_handler(state='order')
@activate_user_language
async def register_order(msg: Message, state: FSMContext, user: TGUser, **kwargs):
    data = await state.get_data()
    product_id = data.get('product_id')
    order = await Order.objects.acreate(
        user=user, product_id=product_id,
        pass_message=msg.text, username=msg.from_user.mention
    )
    await msg.answer(_('Order added to wait list'))
    await send_order_to_admins(msg, order, user)
    await state.finish()


@dp.callback_query_handler(Text(startswith='consultation_'))
@activate_user_language
async def get_consultation(callback: CallbackQuery, **kwargs):
    cancel = InlineKeyboardMarkup().add(InlineKeyboardButton(_('Cancel'), callback_data='cancel'))
    await callback.message.answer(_('Consultation Message'), reply_markup=cancel)

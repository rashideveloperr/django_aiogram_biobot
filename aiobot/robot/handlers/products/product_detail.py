from aiogram.dispatcher.filters import Text
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    ParseMode,
)
from django.utils.translation import gettext as _
from root.settings import HOST

from aiobot.models import Product, ProductImage, TGUser
from aiobot.robot.config import dp
from aiobot.robot.validators import activate_user_language, html_formatter


def image_web_url(url):
    return HOST + url


@dp.callback_query_handler(Text(startswith='product_'))
@activate_user_language
async def product_detail(callback: CallbackQuery, user: TGUser, **kwargs):
    product_id = int(callback.data.replace('product_', ''))
    product = await Product.objects.aget(id=1)

    text = await html_formatter(await product.td_description(user.lang))
    images_count = await ProductImage.objects.filter(product_id=product_id).acount()
    images = [InputMediaPhoto(image_web_url(product.main_image.url), text, ParseMode.HTML)]

    keyboards = InlineKeyboardMarkup(1).add(
        *[
            InlineKeyboardButton(_('Order'), callback_data=f'order_{product_id}'),
            InlineKeyboardButton(_('Get a Consultation'), callback_data=f'consultation_{product_id}')
        ]
    )

    if not images_count:
        await callback.message.answer_photo(images[0].media, text, ParseMode.HTML, reply_markup=keyboards)
        return

    async for item in ProductImage.objects.filter(product_id=product_id):
        images.append(InputMediaPhoto(image_web_url(item.image.url)))

    await callback.message.answer_media_group(images)
    await callback.message.answer(_('Order'), reply_markup=keyboards)
    await callback.message.delete()

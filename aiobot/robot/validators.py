from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from django.utils.translation import activate

from aiobot.models import TGUser


def activate_user_language(func):
    async def wrapper(msg: Union[Message | CallbackQuery], state: FSMContext):
        user = msg.from_user
        _, created = await TGUser.objects.aget_or_create(user_id=user.id)
        activate(_.lang)
        return await func(msg, state=state, user=_, created=created)

    return wrapper


def get_all_translations(text):
    dictionary = {
        'Feedback': ['Fikr-mulohaza', 'Обратная связь', 'Фикр-мулоҳаза'],
        'Products': ['Mahsulotlar', 'Продукты', 'Маҳсулотлар']
    }

    return dictionary.get(text)


def is_msg_equal(msg, text):
    translations = get_all_translations(text)
    return msg.text in translations


async def html_formatter(text: str):
    return text.replace('</p><p>', '\n').replace('<p>', '').replace('</p>', '')

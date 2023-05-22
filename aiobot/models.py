from asgiref.sync import sync_to_async
from django.core.validators import validate_image_file_extension
from django.db import models
from django.db.models import (
    CASCADE,
    SET_NULL,
    BigIntegerField,
    BooleanField,
    CharField,
    CheckConstraint,
    DateTimeField,
    ForeignKey,
    ImageField,
    PositiveIntegerField,
    Q,
)
from django_ckeditor_5.fields import CKEditor5Field
from parler.models import TranslatableModel, TranslatedFields


class TGUser(models.Model):
    class Language(models.TextChoices):
        UZ = 'uz', "O'zbek"
        RU = 'ru', 'Рус'
        CYR = 'cyr', 'Узбек'

    user_id = BigIntegerField(unique=True)
    fullname = CharField(max_length=255, default='Lead User')
    lang = CharField(max_length=30, choices=Language.choices, default='ru', null=False)
    phone_number = CharField(max_length=30)
    is_lead = BooleanField(default=True)
    joined_at = DateTimeField(auto_now_add=True)

    @classmethod
    def update_language(self, user_id, lang):
        user = TGUser.objects.get(user_id=user_id)
        user.lang = lang
        user.save()

    async def async_save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        await sync_to_async(super().save)(force_insert=force_insert, force_update=force_update, using=using,
                                          update_fields=update_fields)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.phone_number:
            if not self.phone_number.startswith('+'):
                self.phone_number = '+' + self.phone_number
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = 'Telegram User'
        verbose_name_plural = 'Telegram Users'


class Product(TranslatableModel, models.Model):
    translations = TranslatedFields(
        name=CharField(max_length=125),
        description=CKEditor5Field('Description', config_name='extends'),
    )
    main_image = ImageField(upload_to='product_images', validators=[validate_image_file_extension])

    async def td_name(self, lang='ru'):
        return await sync_to_async(self.safe_translation_getter)('name', 'ru', lang, True)

    async def td_description(self, lang='ru'):
        return await sync_to_async(self.safe_translation_getter)('description', 'ru', lang, True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = ForeignKey(Product, on_delete=CASCADE, related_name='images')
    image = ImageField(upload_to='product_images', validators=[validate_image_file_extension])
    order = PositiveIntegerField()

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(order__lte=10),
                name='max_image_count'
            )
        ]


class Order(models.Model):
    user = ForeignKey(TGUser, CASCADE)
    product = ForeignKey(Product, SET_NULL, null=True)
    username = CharField(max_length=255)
    pass_message = CharField(max_length=1024)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order of {self.user.user_id}'

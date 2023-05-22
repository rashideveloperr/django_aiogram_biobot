from django.contrib import admin
from django.utils.html import format_html
from parler.admin import TranslatableAdmin

from aiobot.models import Order, Product, ProductImage, TGUser

# Register your models here.

@admin.register(TGUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'fullname', 'lang', 'phone_number')
    list_display_links = ('id', 'user_id')


class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ('id', 'name', 'image')
    inlines = [ProductImageInline]
    list_display_links = ('id', 'name')

    def image(self, obj: Product):
        return format_html(f'<img src="{obj.main_image.url}" width="50px">')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'username', 'pass_message', 'created_at')
    list_display_links = ('id', 'pass_message')

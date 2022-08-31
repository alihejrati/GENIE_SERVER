from django.contrib import admin
from utils import admin as Admin
from apps.tags.models import TaggedItem
from apps.store.models import Product
from apps.store.admin import ModelAdminClass

# Register your models here.

class CustomProductAdmin(ModelAdminClass.ProductAdmin):
    inlines = [TaggedItem.objects.get_inline()]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
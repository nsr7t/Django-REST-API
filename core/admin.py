from store.models import Product
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from tags.models import TaggedItem, Tag
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
    (None,
        {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "email", "first_name", "last_name"),
        },
    ),)
    

class TagAdmin(admin.ModelAdmin):
    search_fields = ['tag']


class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    model_admin = TagAdmin


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
admin.site.register(Tag, TagAdmin)

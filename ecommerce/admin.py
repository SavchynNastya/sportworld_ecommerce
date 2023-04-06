from django.contrib import admin
from .models import Category, Subcategory, Producer, Item

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Producer)
admin.site.register(Item)

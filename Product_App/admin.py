from django.contrib import admin
from .models import State
from .models import City
from .models import Category
from .models import Product
# Register your models here.

admin.site.register(State)
admin.site.register(City)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'status', 'created', 'updated']
    list_filter = ['created', 'updated', 'category']
    list_editable = ['price', 'status']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)



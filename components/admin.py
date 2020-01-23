from django.contrib import admin

from .models import ProductModel

class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic Information', {'fields': ['name', 'desc']}),
        ('Stock Info', {'fields': ['price', 'stock']}),
    ]

# Register your models here.
admin.site.register(ProductModel, ProductAdmin)

from django.contrib import admin
from .models import *

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display=['category_name', 'slug']
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('brand_name',)}
    list_display=['brand_name', 'slug']
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display=['product_name','price','stock','category','is_available']
    prepopulated_fields={'slug':('product_name',)}
class ColorAdmin(admin.ModelAdmin):
    list_display=['color_name','color_code']



# Register your models here.

admin.site.register(User)
admin.site.register(category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(Color)
admin.site.register(ProductAttribute)
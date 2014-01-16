from django.contrib import admin

from .models import Product, Rating

class RatingAdmin(admin.ModelAdmin):
    raw_id_fields = ('product', )

class ProductAdmin(admin.ModelAdmin):
    # Fields to show in list view
    list_display = ('name', 'url', 'category', )
    # Fields we can filter on
    list_filter = ('category', )
    # Fields we can search in admin
    search_fields = ('name', )

admin.site.register(Product, ProductAdmin)
admin.site.register(Rating, RatingAdmin)
from django.contrib import admin

from .models import Stock
# Register your models here.

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'ts_code', 'name', 'area', 'industry', 'market', 'list_status', 'list_date', 'is_hs')
    list_display_links = ('name',)
    list_filter = ('area', 'industry', 'market', 'is_hs', 'list_status',)
    search_fields = ('name', 'ts_code',)
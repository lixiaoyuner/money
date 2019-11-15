from django.contrib import admin

from .models import Stock, DayK
# Register your models here.

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'ts_code', 'name', 'area', 'industry', 'market', 'list_status', 'list_date', 'is_hs')
    list_display_links = ('name',)
    list_filter = ('exchange', 'area', 'industry', 'market', 'is_hs', 'list_status',)
    search_fields = ('name', 'ts_code',)

@admin.register(DayK)
class DayKAdmin(admin.ModelAdmin):
    list_display = ('stock', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount')
    list_display_links = ('trade_date',)
    # list_filter = ('stock', 'trade_date',)
    search_fields = ('stock', 'trade_date', 'pct_chg',)
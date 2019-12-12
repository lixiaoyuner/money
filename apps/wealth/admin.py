from django.contrib import admin
from django.core.paginator import Paginator

from .models import Stock, DayK
# Register your models here.

# class LargeTablePaginator(Paginator):
#     def _get_count(self):
#         return 10000000
#     count = property(_get_count)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'ts_code', 'name', 'area', 'industry', 'market', 'list_status', 'list_date', 'is_hs')
    list_display_links = ('name',)
    list_filter = ('exchange', 'area', 'industry', 'market', 'is_hs', 'list_status',)
    search_fields = ('name', 'ts_code',)

@admin.register(DayK)
class DayKAdmin(admin.ModelAdmin):
    show_full_result_count=False
    # paginator = LargeTablePaginator
    list_display = ('stock_info', 'trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount')
    list_display_links = ('trade_date',)
    # list_select_related = ('stock',)
    search_fields = ('trade_date', 'pct_chg',)
    def stock_info(self, obj):
        return u'%s | %s' % (obj.stock.name, obj.stock.ts_code)
    stock_info.short_description = '对应股票'

    

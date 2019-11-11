import os
import sys

import django
import tushare as ts

# 将项目路径添加到系统搜寻路径当中，查找方式为从当前脚本开始，找到要调用的django项目的路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 设置项目的配置文件 不做修改的话就是 settings 文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yun.settings")
django.setup()  # 加载项目配置

from django.conf import settings
from wealth.models import Stock

ts_pro = ts.pro_api(settings.TUSHARE_TOKEN)
stocks = ts_pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
for stock in stocks:
    print(type(stock), stock)
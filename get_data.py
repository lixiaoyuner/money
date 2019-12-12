import os
import sys
import datetime
import time
import pickle
from functools import reduce

import django
import tushare as ts
import pandas as pd
from tqdm import tqdm

# 将项目路径添加到系统搜寻路径当中，查找方式为从当前脚本开始，找到要调用的django项目的路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 设置项目的配置文件 不做修改的话就是 settings 文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yun.settings")
django.setup()  # 加载项目配置

from django.conf import settings
# from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from wealth.models import Stock, DayK


tushare_token = settings.TUSHARE_TOKEN
ts_pro = ts.pro_api(tushare_token)

def clock_deco(func):
    def inner(*args, **kwargs):
        start = datetime.datetime.now()
        func(*args, **kwargs)
        print((datetime.datetime.now() - start).seconds)
    return inner

def get_stock_info():
    stocks = ts_pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
    columns = stocks.columns
    for stock in tqdm(stocks.values):
        args = {key: value for key, value in zip(columns, stock)}
        args['list_date'] = datetime.datetime.strptime(args['list_date'], '%Y%m%d')
        args['delist_date'] = datetime.datetime.strptime(args['delist_date'], '%Y%m%d') if args['delist_date'] else None
        try:
            Stock.objects.update_or_create(ts_code=args['ts_code'], defaults=args)
        except Exception as error:
            print('写入数据库失败，原因', error)

@clock_deco
def get_stock_dayk():
    stocks = Stock.objects.filter(list_status='L')
    for index, stock in enumerate(stocks):
        start_date = stock.list_date.strftime('%Y%m%d')
        end_date = datetime.datetime.now().strftime('%Y%m%d')
        dayks = None
        while int(end_date) >= int(start_date):
            dayks_tmp = ts_pro.daily(ts_code=stock.ts_code,start_date=start_date, end_date=str(int(start_date) + 10*10000)).iloc[::-1]
            dayks = pd.concat([dayks, dayks_tmp], ignore_index=True) if dayks is not None else dayks_tmp
            # dayks = dayks_tmp if dayks is None else dayks.append(dayks_tmp, ignore_index=True)
            start_date = str(int(start_date) + 100001)
        dayks.drop(columns = ['ts_code',], inplace=True)
        print(dayks)
        columns = dayks.columns
        for dayk in tqdm(dayks.values):
            args = {key: value for key, value in zip(columns, dayk)}
            args['trade_date'] = datetime.datetime.strptime(args['trade_date'], '%Y%m%d')
            args['stock'] = stock
            try:
                # DayK.objects.update_or_create(stock=stock, trade_date=args['trade_date'], defaults=args)
                DayK.objects.create(**args)
            except Exception as error:
                print('写入数据库失败，原因', error)
        # if index and index % 60 == 0:
        #     for i in tqdm(range(23)):
        #         time.sleep(1)

@clock_deco
def update_dayk():
    end_date = int(datetime.datetime.now().strftime('%Y%m%d')) + 1
    start_date = end_date - 17
    dayks = None
    for date in range(start_date, end_date):
        dayks_tmp = ts_pro.daily(trade_date=str(date))
        dayks = pd.concat([dayks, dayks_tmp], ignore_index=True) if dayks is not None else dayks_tmp
    print(dayks)
    columns = dayks.columns
    for dayk in tqdm(dayks.values):
        args = {key: value for key, value in zip(columns, dayk)}
        args['trade_date'] = datetime.datetime.strptime(args['trade_date'], '%Y%m%d')
        try:
            args['stock'] = Stock.objects.get(ts_code=args['ts_code'])
            del(args['ts_code'])
        except ObjectDoesNotExist as error:
            print(args)
        try:
            DayK.objects.get_or_create(stock=args['stock'], trade_date=args['trade_date'], defaults=args)
            # DayK.objects.create(**args)
        except Exception as error:
            print('写入数据库失败，原因', error)

def remove_data():
    dayks = DayK.objects.filter(trade_date__gte=datetime.datetime(2019,11,1)).delete()
    print(dayks)

def get_front_data(stock, trade_date):
    tmp = [(int(stock.symbol),)]
    trade_date = trade_date
    while len(tmp) != 3:
        dayk = DayK.objects.filter(stock=stock).filter(trade_date=trade_date-datetime.timedelta(1))
        trade_date -= datetime.timedelta(1)
        if trade_date < stock.list_date:
            return []
        tmp = tmp + list(dayk.values_list('open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount')) if dayk else tmp
    return reduce(lambda x,y: x + y, tmp)

def get_train_data():
    train_set_x = []
    train_set_y = []
    dayks = DayK.objects.filter(trade_date__gte=datetime.datetime(2019,1,1))
    for dayk in tqdm(dayks):
        stock = dayk.stock
        trade_date = dayk.trade_date
        if stock.market == '科创板':
            continue
        tmp = get_front_data(stock, trade_date)
        if not tmp:
            continue
        train_set_x.append(tmp)
        if dayk.pct_chg <= 0:
            train_set_y.append(0)
        elif dayk.pct_chg <= 9:
            train_set_y.append(1)
        else:
            train_set_y.append(2)
    
    # print(train_set_x, train_set_y)
    with open('/root/Documents/train_set_x.pickle', 'wb+') as f:
        pickle.dump(train_set_x, f)
    with open('/root/Documents/train_set_y.pickle', 'wb+') as f:
        pickle.dump(train_set_y, f)
    return train_set_x, train_set_y

if __name__ == '__main__':
    # get_stock_info()
    # get_stock_dayk()
    # update_dayk()
    # remove_data()
    get_train_data()
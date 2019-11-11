from django.db import models

# Create your models here.

class Stock(models.Model):
    '''
    上交所和深交所所有股票
    '''
    id = models.AutoField(primary_key=True)
    ts_code = models.CharField(verbose_name='TS代码', max_length=100)
    symbol = models.CharField(verbose_name='股票代码', max_length=100)
    name = models.CharField(verbose_name='股票名称', max_length=100)
    area = models.CharField(verbose_name='所在地域', max_length=100)
    industry = models.CharField(verbose_name='所属行业', max_length=100)
    fullname = models.CharField(verbose_name='股票全称', max_length=100)
    enname = models.CharField(verbose_name='英文全称', max_length=100)
    market = models.CharField(verbose_name='市场类型', max_length=100)
    exchange = models.CharField(verbose_name='交易所代码', max_length=100)
    curr_type = models.CharField(verbose_name='交易货币', max_length=100)
    list_status = models.CharField(verbose_name='上市状态', max_length=100, help_text='L上市 D退市 P暂停上市')
    list_date = models.CharField(verbose_name='上市日期', max_length=100)
    delist_date = models.CharField(verbose_name='退市日期', max_length=100, null=True)
    is_hs = models.CharField(verbose_name='是否沪深港通', max_length=100, help_text='N否 H沪股通 S深股通')

    def __str__(self):
        return f'{self.name} | {self.symbol}'

    class Meta:
        ordering = ('id',)
        verbose_name = '所有股票基本信息'
        verbose_name_plural = '所有股票基本信息'

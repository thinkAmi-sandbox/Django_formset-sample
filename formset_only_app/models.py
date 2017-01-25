from django.db import models


class Item(models.Model):
    name = models.CharField('品名', max_length=100)
    quantity = models.IntegerField('数量')
    unit_price = models.PositiveIntegerField('単価')

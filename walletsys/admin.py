# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from walletsys.models import Balance, TransactionDetail

# Register your models here.


class BalanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'uid', 'balance']


class TransactionDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'transaction_type', 'amount', 'oid', 'uid']


admin.site.register(Balance, BalanceAdmin)
admin.site.register(TransactionDetail, TransactionDetailAdmin)

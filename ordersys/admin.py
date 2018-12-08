# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from ordersys.models import OrderInfo, OrderCancelReason, OrderProductTypeBind, OrderReasonBind, OrderProductType

# Register your models here.


class CTypeBind(admin.TabularInline):
    extra = 1
    verbose_name = u"C端记账账单"
    model = OrderProductTypeBind


class BTypeBind(admin.TabularInline):
    extra = 1
    verbose_name = u"B端记账账单"
    model = OrderProductType


class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid_c', 'uid_b', 'o_state', 'amount', 'c_delivery_info', 'create_time')
    list_editable = ('o_state', 'uid_c', 'uid_b', 'amount')
    list_display_links = ('id', )

    inlines = [CTypeBind, BTypeBind]


admin.site.register(OrderInfo, OrderInfoAdmin)
admin.site.register([OrderCancelReason, OrderProductTypeBind, OrderReasonBind, OrderProductType])

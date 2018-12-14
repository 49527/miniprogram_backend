# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.timezone import now
from ordersys.models import OrderInfo, OrderCancelReason, OrderProductTypeBind, OrderCancelReasonBind, OrderProductType

# Register your models here.


class CTypeBind(admin.TabularInline):
    extra = 1
    verbose_name = u"C端记账账单"
    model = OrderProductTypeBind


class BTypeBind(admin.TabularInline):
    extra = 1
    verbose_name = u"B端记账账单"
    model = OrderProductType


class DispatchFilter(SimpleListFilter):
    title = 'time'
    parameter_name = 'time'

    def lookups(self, request, model_admin):
        return [(1, "3分钟"), (2, "5分钟"), (3, "10分钟"), (4, "15分钟")]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        if int(self.value()) == 1:
            return queryset.filter(create_time__gte=(now()+datetime.timedelta(minutes=3)).strftime("%Y-%m-%d %H:%M:%S"))

        if int(self.value()) == 2:
            return queryset.filter(create_time__gte=(now()+datetime.timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S"))

        if int(self.value()) == 3:
            return queryset.filter(create_time__gte=(now()+datetime.timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S"))

        if int(self.value()) == 4:
            return queryset.filter(create_time__gte=(now()+datetime.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S"))


class OrderInfoAdmin(admin.ModelAdmin):
    readonly_fields = ('create_time', )
    list_display = ('id', 'uid_c', 'uid_b', 'o_state', 'amount', 'c_delivery_info', 'create_time')
    list_editable = ('o_state', 'uid_c', 'uid_b', 'amount')
    list_display_links = ('id', )
    list_filter = (DispatchFilter, )

    inlines = [CTypeBind, BTypeBind]


admin.site.register(OrderInfo, OrderInfoAdmin)
admin.site.register([OrderCancelReason, OrderProductTypeBind, OrderCancelReasonBind, OrderProductType])

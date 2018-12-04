# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from ordersys.models import OrderInfo, OrderCancelReason, OrderProductTypeBind, OrderReasonBind

# Register your models here.

admin.site.register([OrderInfo, OrderCancelReason, OrderProductTypeBind, OrderReasonBind])

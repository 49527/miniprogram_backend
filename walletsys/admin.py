# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from walletsys.models import Balance, TransactionDetail

# Register your models here.
admin.site.register([Balance, TransactionDetail])

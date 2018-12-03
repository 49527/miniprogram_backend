# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from category_sys.models import ProductSubType, ProductTopType


# Register your models here.

admin.site.register([ProductSubType, ProductTopType])

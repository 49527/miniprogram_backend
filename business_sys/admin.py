# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from business_sys.models import RecycleBin, RecyclingStaffInfo, BusinessProductTypeBind, RecyclingStaffInfoGps
from django.contrib import admin

# Register your models here.


class BusinessProductTypeBindInline(admin.TabularInline):
    model = BusinessProductTypeBind


class RecycleBinAdmin(admin.ModelAdmin):
    inlines = [BusinessProductTypeBindInline]


admin.site.register(RecycleBin, RecycleBinAdmin)
admin.site.register([RecyclingStaffInfo, BusinessProductTypeBind])
admin.site.register([RecyclingStaffInfoGps])

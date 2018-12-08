# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from category_sys.models import ProductSubType, ProductTopType


# Register your models here.

class SubTypeInline(admin.TabularInline):
    model = ProductSubType


class TopTypeAdmin(admin.ModelAdmin):
    list_display = ('t_top_name', 'operator')
    list_editable = ('in_use', )
    list_filter = ('operator', )
    inlines = (SubTypeInline, )


admin.site.register(ProductTopType, TopTypeAdmin)
admin.site.register([ProductSubType])

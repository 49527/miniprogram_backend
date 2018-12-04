# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from business_sys.models import RecycleBin, RecyclingStaffInfo, BusinessProductTypeBind
from django.contrib import admin

# Register your models here.

admin.site.register([RecycleBin, RecyclingStaffInfo, BusinessProductTypeBind])

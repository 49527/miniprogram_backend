# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from usersys.models import UserBase, UserSid

# Register your models here.
admin.site.register([UserBase, UserSid])

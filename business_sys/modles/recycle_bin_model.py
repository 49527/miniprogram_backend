# coding=UTF-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models

from business_sys.choices.model_choices import recycle_bin_type

class RecycleBin(models.Model):
    GPS_L = models.FloatField(_("经度"))
    GPS_A = models.FloatField(_("纬度"))
    rb_name = models.CharField(_("回收站名称"), max_length=100)
    r_b_type = models.IntegerField(_("回收站类型"), choices=recycle_bin_type.choice)
    loc_desc = models.TextField(_("地点描述"))
    create_time = models.DateTimeField(auto_now_add=True)
    pn = models.CharField(_("联系电话"), max_length=20)

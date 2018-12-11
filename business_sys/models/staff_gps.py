# coding=UTF-8
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _

from usersys.models import UserBase


class RecyclingStaffInfoGps(models.Model):
    uid = models.OneToOneField(
        UserBase,
        related_name="staff_info_gps",
        verbose_name=_("用户id"),
    )
    lat = models.FloatField()
    lng = models.FloatField()
    create_time = models.DateTimeField(verbose_name=_('创建时间'), auto_now_add=True)

    def __unicode__(self):
        return u"{}-{}-{}".format(self.uid, self.lat, self.lng)

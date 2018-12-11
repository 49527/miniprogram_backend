# coding=UTF-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from usersys.models import UserBase


class RecyclingStaffInfoGps(models.Model):
    uid = models.OneToOneField(
        UserBase,
        related_name="staff_info_gps",
        verbose_name=_("用户id"),
    )
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    create_time = models.DateTimeField(_('创建时间'), auto_now_add=True)

    def __unicode__(self):
        return u"{}-{}-{}".format(self.uid, self.lat, self.lng)

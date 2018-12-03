# coding=UTF-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from category_sys.choices.model_choices import top_type_choice, type_unit_choice


class ProductTopType(models.Model):
    t_top_name = models.CharField(max_length=20)
    in_use = models.BooleanField(default=True)
    operator = models.IntegerField(_("所属端类型"), choices=top_type_choice.choice)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.t_top_name


class ProductSubType(models.Model):
    t_sub_name = models.CharField(max_length=20)
    in_use = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    unit = models.IntegerField(_("计价单位"), choices=type_unit_choice.choice)
    toptype_c = models.ForeignKey(
        ProductTopType,
        verbose_name=_("C端顶级品类"),
        related_name="c_subtype"
    )
    toptype_b = models.ForeignKey(
        ProductTopType,
        verbose_name=_("B端顶级品类"),
        related_name="b_subtype"
    )

    def __unicode__(self):
        return self.t_sub_name

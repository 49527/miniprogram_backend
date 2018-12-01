# coding=UTF-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from category_sys.choices.model_choices import top_type_choice, type_unit_choice


class ProductTopType(models.Model):
    t_top_name = models.CharField(max_length=20)
    in_use = models.BooleanField(default=True)
    Operator = models.IntegerField(_("所属端类型"), choices=top_type_choice.choice)
    create_time = models.DateTimeField(auto_now_add=True)


class ProductSubType(models.Model):
    t_sub_name = models.CharField(max_length=20)
    in_use = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    unit = models.IntegerField(_("计价单位"), choices=top_type_choice.choice)


class TopSubBind(models.Model):
    top_type = models.ForeignKey(
        ProductTopType,
        verbose_name=_("顶级品类"),
        related_name="top2sub"
    )
    sub_type = models.ForeignKey(
        ProductSubType,
        verbose_name=_("二级品类"),
        related_name="sub2top"
    )

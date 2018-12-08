# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from category_sys.models import ProductSubType, ProductTopType
from category_sys.choices.model_choices import top_type_choice


# Register your models here.

class SubTypeInlineC(admin.TabularInline):
    model = ProductSubType
    extra = 1
    fk_name = "toptype_c"


class SubTypeInlineB(admin.TabularInline):
    model = ProductSubType
    extra = 1
    fk_name = "toptype_b"


class TopTypeAdmin(admin.ModelAdmin):
    list_display = ('t_top_name', 'operator', 'in_use')
    list_editable = ('in_use', )
    list_filter = ('operator', )

    def get_inline_instances(self, request, obj=None):
        # type: (object, ProductTopType) -> object

        # Dynamic inline based on top type operator
        if obj is not None:
            if obj.operator == top_type_choice.CONSUMER:
                self.inlines = [SubTypeInlineC]

            if obj.operator == top_type_choice.BUSINESS:
                self.inlines = [SubTypeInlineB]

        return super(TopTypeAdmin, self).get_inline_instances(request, obj)


admin.site.register(ProductTopType, TopTypeAdmin)
admin.site.register([ProductSubType])

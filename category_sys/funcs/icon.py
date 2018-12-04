# coding=UTF-8
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from base.exceptions import WLException
from category_sys.models import ProductTopType


def obtain_top_type_photo(top_type):
    # type: (ProductTopType) -> object

    def default_image():
        raise WLException(404, _("无此ICON"))

    try:
        if top_type is not None:
            return open(top_type.icon.path, 'r')
        else:
            return default_image()

    except IOError:
        return default_image()

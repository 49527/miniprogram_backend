from django.conf.urls import url, include

from category_sys.views.icon import ObtainCategoryIconView


icon_urls = [
    url(r'^obtain/$', ObtainCategoryIconView.as_view())
]


urlpatterns = [
    url(r'^icon/', include(icon_urls)),
    ]

from django.conf.urls import url, include
from category_sys.views.icon import ObtainCategoryIconView
from category_sys.views import CategoryListView


icon_urls = [
    url(r'^obtain/$', ObtainCategoryIconView.as_view())
]


urlpatterns = [
    url(r'^icon/', include(icon_urls)),
    url(r'^obtain/category_list/$', CategoryListView.as_view()),
]

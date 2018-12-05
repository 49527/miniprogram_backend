from django.conf.urls import url, include
from category_sys.views import CategoryListView


urlpatterns = [
    url(r'^obtain/category_list/', CategoryListView.as_view()),
]

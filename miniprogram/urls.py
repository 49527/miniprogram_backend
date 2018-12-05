"""miniprogram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
import usersys.urls
import walletsys.urls
import ordersys.urls
import appearancesys.urls
import category_sys.urls
import business_sys.urls

urlpatterns = [
    url(r'^bg/', admin.site.urls),
    url(r'^user/', include(usersys.urls.urlpatterns)),
    url(r'^wallet/', include(walletsys.urls.urlpatterns)),
    url(r'^order/', include(ordersys.urls.urlpatterns)),
    url(r'^appearance/', include(appearancesys.urls.url_patterns)),
    url(r'^category/', include(category_sys.urls.urlpatterns)),
    url(r'^business/', include(business_sys.urls.urlpatterns)),
]

from django.conf.urls import url, include
from usersys.views import login


login_urls = [
    url(r'^login/$', login.LoginView.as_view()),
    url(r'^submit_pn/$', login.SubmitPnView.as_view()),
    url(r'^validate/$', login.PNvalidateView.as_view()),
    url(r'^logout/$', login.LogoutView.as_view()),
]

validate_urls = [

]

urlpatterns = [
    url(r'^login/', include(login_urls)),
    url(r'^validate/', include(validate_urls)),
]

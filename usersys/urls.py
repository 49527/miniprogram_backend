from django.conf.urls import url, include
from usersys.views import login, obtain


login_urls = [
    url(r'^login/$', login.ClientLoginView.as_view()),
    url(r'^submit_pn/$', login.ClientSubmitPnView.as_view()),
    url(r'^validate/$', login.PNvalidateView.as_view()),
    url(r'^logout/$', login.LogoutView.as_view()),
]

validate_urls = [

]

obtain_urls =[
    url(r'self_info/$', obtain.ObtainSelfInfoView.as_view()),
    url(r'qr_info/$', obtain.QRInfoView.as_view()),
]

urlpatterns = [
    url(r'^login/', include(login_urls)),
    url(r'^validate/', include(validate_urls)),
    url(r'^obtain/', include(obtain_urls)),
]

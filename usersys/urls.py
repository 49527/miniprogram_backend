from django.conf.urls import url, include
from usersys.views import login, obtain


login_urls = [
    url(r'^login/$', login.ClientLoginView.as_view()),
    url(r'^submit_pn/$', login.ClientSubmitPnView.as_view()),
    url(r'^validate/$', login.PNvalidateView.as_view()),
    url(r'^logout/$', login.LogoutView.as_view()),
    url(r'^login_b/$', login.RecyclingStaffLoginView.as_view()),
    url(r'^send_sms/$', login.SendSMSView.as_view()),
    url(r'^forget_psw/$', login.ForgetPwdView.as_view()),

]

validate_urls = [

]

obtain_urls =[
    url(r'self_info/$', obtain.ObtainSelfInfoView.as_view()),
]

urlpatterns = [
    url(r'^login/', include(login_urls)),
    url(r'^validate/', include(validate_urls)),
    url(r'^obtain/', include(obtain_urls)),
]

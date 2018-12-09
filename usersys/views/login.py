# coding=utf-8
from rest_framework.views import APIView
from base.views import WLAPIView
from base.util.get_ip import get_client_ip
from usersys.funcs.login import wechat_login, get_sid_by_pn, validate_sid, logout, recycling_staff_login, send_sms, \
    forget_pwd
from usersys.serializers.login_api import (
    LoginSerializer, SubmitPnSerializer, PNvalidateSerializer,
    LogoutSerializer, RecyclingStaffLoginSerializer, SendSerializer,
    ForgetPwdSerializer
)


class ClientLoginView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = LoginSerializer(data=data)
        self.validate_serializer(seri)

        sid, state = wechat_login(ipaddr=get_client_ip(request), **seri.data)
        return self.generate_response(
            data={
                "user_sid": sid,
                "state": state
            },
            context=context
        )


class ClientSubmitPnView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = SubmitPnSerializer(data=data)
        self.validate_serializer(seri)

        sid = get_sid_by_pn(seri.data['pn'])
        return self.generate_response(
            data={
                'pn': seri.data['pn'],
                'user_sid': seri.data['user_sid'],
                'sid': sid
            },
            context=context
        )


class PNvalidateView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = PNvalidateSerializer(data=data)
        self.validate_serializer(seri)

        validate_sid(**seri.data)

        return self.generate_response(
            data={
                "pn": seri.data['pn'],
                "user_sid": seri.data['user_sid']
            },
            context=context
        )


class LogoutView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = LogoutSerializer(data=data)
        self.validate_serializer(seri)

        logout(**seri.data)
        return self.generate_response(
            data={},
            context=context
        )


class RecyclingStaffLoginView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = RecyclingStaffLoginSerializer(data=data)
        self.validate_serializer(seri)
        user_sid, recycle_bin_type = recycling_staff_login(ipaddr=get_client_ip(request), **seri.data)
        return self.generate_response(
            data={
                'pn': seri.data.get('pn'),
                'user_sid': user_sid,
                'recycle_bin_type': recycle_bin_type,
            },
            context=context
        )


class SendSMSView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = SendSerializer(data=data)
        self.validate_serializer(seri)
        send_sms(**seri.data)
        return self.generate_response(
            data={
                'pn': seri.data.get('pn'),
            },
            context=context
        )


class ForgetPwdView(WLAPIView, APIView):
    def post(self, request):
        data, context = self.get_request_obj(request)
        seri = ForgetPwdSerializer(data=data)
        self.validate_serializer(seri)
        forget_pwd(**seri.data)
        return self.generate_response(
            data={
                'msg': u'密码已重置',
            },
            context=context
        )

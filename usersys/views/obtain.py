from rest_framework.views import APIView
from base.views import WLAPIView
from usersys.serializers.obtain_api import ObtainSelfInfoSerializer
from usersys.serializers.usermodel import UserInfoDisplay
from usersys.funcs.obtain import obtain_self_info


class ObtainSelfInfoView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainSelfInfoSerializer(data=data)
        self.validate_serializer(seri)

        user_info, is_validate = obtain_self_info(**seri.data)
        seri_u_info = UserInfoDisplay(user_info)
        return self.generate_response(
            data={
                "user_info": seri_u_info.data,
                "is_validate": is_validate
            },
            context=context
        )

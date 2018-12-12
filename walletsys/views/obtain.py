from rest_framework.views import APIView
from base.views import WLAPIView
from walletsys.serializers.obtain_api import ObtainBalanceSerializer, ObtainHistorySerializer
from walletsys.funcs.obtain import obtain_balance, obtain_history
from walletsys.serializers.wallet import TransactionDetailDisplay
from django.conf import settings
COUNT_PER_PAGE = settings.COUNT_PER_PAGE


class ObtainBalanceView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainBalanceSerializer(data=data)
        self.validate_serializer(seri)

        balance = obtain_balance(**seri.data)
        return self.generate_response(
            data={
                "balance": balance
            },
            context=context
        )


class ObtainHistoryView(WLAPIView, APIView):
    def get(self, request):
        data, context = self.get_request_obj(request)
        seri = ObtainHistorySerializer(data=data)
        self.validate_serializer(seri)

        history, n_pages = obtain_history(count_per_page=COUNT_PER_PAGE, **seri.data)

        seri_history = TransactionDetailDisplay(history, many=True)

        return self.generate_response(
            data={
                "history": seri_history.data,
                "n_pages": n_pages
            },
            context=context
        )

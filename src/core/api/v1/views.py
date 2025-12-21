from adrf.views import APIView
from asgiref.sync import sync_to_async
from rest_framework.response import Response

from core.services import convert_amount, get_currency_rates
from .serializers import ConvertAmountQuerySerializer, CurrencyRatesTimeSeriesQuerySerializer


class CurrencyRatesTimeSeriesView(APIView):
    async def get(self, request) -> Response:
        serializer = CurrencyRatesTimeSeriesQuerySerializer(data=request.query_params)
        await sync_to_async(serializer.is_valid)(raise_exception=True)
        query_params = serializer.validated_data

        currency_rates = await get_currency_rates(
            query_params['source_currency'],
            query_params['date_from'],
            query_params['date_to'],
        )

        return Response(currency_rates)


class ConvertAmountView(APIView):
    async def get(self, request) -> Response:
        serializer = ConvertAmountQuerySerializer(data=request.query_params)
        await sync_to_async(serializer.is_valid)(raise_exception=True)
        query_params = serializer.validated_data

        converted_value = await convert_amount(
            query_params['source_currency'],
            query_params['exchanged_currency'],
            query_params['amount'],
        )

        return Response({'value': converted_value})

import datetime

from django.utils import timezone
from rest_framework import serializers

from core.models import Currency


def validate_date_from_range(value, min_date, max_date):
    if value < min_date:
        raise serializers.ValidationError(f'The date before {min_date} is not supported.')
    if value > max_date:
        raise serializers.ValidationError(f'The date after {max_date} is not supported.')
    return value


class CurrencyRatesTimeSeriesQuerySerializer(serializers.Serializer):
    MIN_SUPPORTED_DATE = datetime.date(1970, 1, 1)

    source_currency = serializers.SlugRelatedField(queryset=Currency.objects.all(), slug_field='code')
    date_from = serializers.DateField()
    date_to = serializers.DateField()

    def validate_date_from(self, value):
        today = timezone.now().date()
        return validate_date_from_range(value, self.MIN_SUPPORTED_DATE, today)

    def validate_date_to(self, value):
        today = timezone.now().date()
        return validate_date_from_range(value, self.MIN_SUPPORTED_DATE, today)

    def validate(self, attrs):
        self._validate_date_range_correctness(attrs)

        return attrs

    @staticmethod
    def _validate_date_range_correctness(attrs):
        date_from = attrs['date_from']
        date_to = attrs['date_to']

        if date_from > date_to:
            raise serializers.ValidationError('"date_from" can not be greater than "date_to".')


class ConvertAmountQuerySerializer(serializers.Serializer):
    source_currency = serializers.SlugRelatedField(queryset=Currency.objects.all(), slug_field='code')
    amount = serializers.DecimalField(max_digits=20, decimal_places=2)
    exchanged_currency = serializers.SlugRelatedField(queryset=Currency.objects.all(), slug_field='code')

    def validate(self, attrs):
        self._validate_source_currency_differs_from_exchanged_currency(attrs)

        return attrs

    @staticmethod
    def _validate_source_currency_differs_from_exchanged_currency(attrs):
        source_currency = attrs['source_currency']
        exchanged_currency = attrs['exchanged_currency']

        if source_currency.code == exchanged_currency.code:
            raise serializers.ValidationError('Source currency and exchanged currency must be different.')

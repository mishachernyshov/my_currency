import asyncio
from http import HTTPStatus

from asgiref.sync import sync_to_async
from django import forms
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from core.models import Currency
from core.services import convert_amount


class CurrencyForm(forms.Form):
    currency = forms.ModelChoiceField(queryset=Currency.objects.all())
    value = forms.DecimalField(decimal_places=6, max_digits=18)

    def __init__(self, *args, currency_label=_('Currency'), is_output_form=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'].label = currency_label
        self.fields['value'].disabled = is_output_form
        self.fields['value'].required = not is_output_form


CurrencyFormSet = formset_factory(CurrencyForm, min_num=1, validate_min=True, extra=0)


async def currency_converter_view(request):
    if request.method == 'GET':
        return await render_initial_conversion_page(request)
    elif request.method == 'POST':
        return await convert_currencies(request)
    else:
        return HttpResponse(status=HTTPStatus.METHOD_NOT_ALLOWED)


async def render_initial_conversion_page(request):
    source_currency_form = CurrencyForm(
        initial={'currency': await Currency.objects.afirst(), 'value': 1},
        currency_label=_('Source currency'),
    )

    context = {
        'source_currency_form': source_currency_form,
        'exchanged_currency_formset': CurrencyFormSet(form_kwargs={
            'currency_label': _('Exchanging currency'),
            'is_output_form': True,
        }),
    }
    return await sync_to_async(render)(request, 'admin/currency_converter.html', context)


async def convert_currencies(request):
    data = request.POST
    source_currency_form = CurrencyForm(
        {'currency': data.get('currency', ''), 'value': data.get('value', '')},
        currency_label=_('Source currency'),
    )
    exchanged_currency_formset = CurrencyFormSet(
        data,
        form_kwargs={'currency_label': _('Exchanging currency'), 'is_output_form': True}
    )

    if (
        await sync_to_async(source_currency_form.is_valid)()
        and await sync_to_async(exchanged_currency_formset.is_valid)()
    ):
        converted_amounts = await asyncio.gather(*[
            convert_amount(
                source_currency_form.cleaned_data['currency'],
                exchanged_currency_form.cleaned_data['currency'],
                source_currency_form.cleaned_data['value']
            )
            for exchanged_currency_form in exchanged_currency_formset
        ])
        exchanged_currency_forms_data = [
            {'currency': exchanged_currency_form.cleaned_data['currency'], 'value': converted_amount}
            for exchanged_currency_form, converted_amount in zip(exchanged_currency_formset, converted_amounts)
        ]
        exchanged_currency_formset = CurrencyFormSet(
            initial=exchanged_currency_forms_data,
            form_kwargs={
                'currency_label': _('Exchanging currency'),
                'is_output_form': True,
            }
        )

    context = {
        'source_currency_form': source_currency_form,
        'exchanged_currency_formset': exchanged_currency_formset,
    }
    return await sync_to_async(render)(request, 'admin/currency_converter.html', context)

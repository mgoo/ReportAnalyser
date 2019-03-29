from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from info_extractor.lib.market_data_loader import data_saver_csv
from info_extractor.models import Market, MarketData


def add_market_form(request):
    template = loader.get_template('info_extractor/markets/add.html')
    return HttpResponse(template.render({}, request))


def add_market(request):
    market_obj = Market(name=request.POST.get('name'))
    market_obj.save()
    return HttpResponseRedirect(reverse('info_extractor:market_view', args=(market_obj.id,)))


def market_list(request):
    template = loader.get_template('info_extractor/markets/list.html')
    markets = Market.objects.all()
    return HttpResponse(template.render({'markets': markets}, request))


def market(request, market_id):
    market = get_object_or_404(Market, id=market_id)
    template = loader.get_template('info_extractor/markets/view.html')
    return HttpResponse(template.render({'market': market}, request))


def upload_data_form(request, market_id):
    market = get_object_or_404(Market, id=market_id)
    template = loader.get_template('info_extractor/markets/upload_data.html')
    return HttpResponse(template.render({'market': market}, request))


def upload_data(request, market_id):
    market = get_object_or_404(Market, id=market_id)
    if 'inflation' in request.FILES:
        data_saver_csv(request.FILES['inflation'], market.name, 'inflation')

    return HttpResponseRedirect(reverse('info_extractor:market_view', args=(market.id,)))

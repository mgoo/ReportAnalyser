from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from info_extractor.lib.market_data_loader import *
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
    if 'cpi' in request.FILES:
        data_saver_csv(request.FILES['cpi'], market.name, 'cpi')

    data_loader = get_data_loader(market.name)
    data = data_loader(market.name)

    for row in data:
        if MarketData.objects.filter(market_id=market.id, date=row['date'], measure=row['measure']).exists():
            continue

        MarketData(
            market_id=market.id,
            date=row['date'],
            measure=row['measure'],
            value=row['value']
        ).save()

    return HttpResponseRedirect(reverse('info_extractor:market_view', args=(market.id,)))

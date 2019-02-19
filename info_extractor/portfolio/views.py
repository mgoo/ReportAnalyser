from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.urls import reverse

from info_extractor.models import Transaction, Instrument


def transactions(request):
    transaction_list = Transaction.objects.all()
    template = loader.get_template('info_extractor/portfolio/transactions.html')
    return HttpResponse(template.render({'transactions': transaction_list}, request))


def current_position(request):
    # TODO
    template = loader.get_template('info_extractor/portfolio/currrent_position.html')
    return HttpResponse(template.render({}, request))


def add_transaction(request):
    template = loader.get_template('info_extractor/portfolio/add_transaction.html')
    instruments = Instrument.objects.all()
    return HttpResponse(template.render({'instruments': instruments}, request))


def process_add_transaction(request):
    instrument = get_object_or_404(Instrument, id = request.POST.get('instrument'))
    amount = request.POST.get('amount')
    price = request.POST.get('price')
    date = request.POST.get('date')

    transaction = Transaction(
        instrument_id=instrument.id,
        amount=amount,
        price=price,
        date=date
    )
    transaction.save()

    return HttpResponseRedirect(reverse('info_extractor:portfolio_position'))
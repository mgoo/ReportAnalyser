import datetime

from django.http import HttpResponse
from django.http.request import QueryDict
from django.shortcuts import get_object_or_404
from django.template import loader

from info_extractor.metrics import *
from info_extractor.models import Instrument


def home(request):
    template = loader.get_template('info_extractor/compare/home.html')

    return HttpResponse(template.render({}, request))


def compare_time_period(request):
    template = loader.get_template('info_extractor/compare/time_period.html')

    context = {}

    context['available_metrics'] = [
        {'name': metric().get_name(), 'class_name': metric().__class__.__name__}
        for metric in SingleMetric.__subclasses__()
    ]

    context['instruments'] = Instrument.objects.all()

    return HttpResponse(template.render(context, request))


def compare_time_period_results(request):
    template = loader.get_template('info_extractor/compare/time_period_results.html')
    instruments = [
        get_object_or_404(Instrument, id=instrument_id)
        for instrument_id in request.POST.getlist('instruments')
    ]
    metrics = [globals()[metric]() for metric in request.POST.getlist('metrics')]
    start_date = datetime.datetime.strptime(request.POST['start-date'], '%Y-%m-%d %H:%M')
    end_date = datetime.datetime.strptime(request.POST['end-date'], '%Y-%m-%d %H:%M')

    titles = ['Instrument'] + [metric.get_name() for metric in metrics]
    data = []
    for instrument in instruments:
        instrument_data = ["%s - %s" % (instrument.name, instrument.market.name)]
        for metric in metrics:
            try:
                metric_value = round(metric.process(instrument, start_date, end_date), 2)
            except Exception as e:
                metric_value = '-'
                print(e)
            instrument_data.append(metric_value)
        data.append(instrument_data)

    context = {
        'titles': titles,
        'data': data
    }
    return HttpResponse(template.render(context, request))


def compare_time_series(request):
    template = loader.get_template('info_extractor/compare/time_series.html')

    context = {}

    context['available_metrics'] = [
        {'name': metric().get_name(), 'class_name': metric().__class__.__name__}
        for metric in OverTimeMetric.__subclasses__()
    ]

    context['instruments'] = Instrument.objects.all()

    return HttpResponse(template.render(context, request))


def compare_time_series_results(request):
    template = loader.get_template('info_extractor/compare/time_series_results.html')
    instruments = [
        get_object_or_404(Instrument, id=instrument_id)
        for instrument_id in request.POST.getlist('instruments')
    ]
    metrics = [globals()[metric]() for metric in request.POST.getlist('metrics')]
    start_date = datetime.datetime.strptime(request.POST['start-date'], '%Y-%m-%d %H:%M')
    end_date = datetime.datetime.strptime(request.POST['end-date'], '%Y-%m-%d %H:%M')

    data = []
    for metric in metrics:
        data.append([])
        for instrument in instruments:
            try:
                metric_value = metric.process(instrument, start_date, end_date)
            except Exception as e:
                metric_value = '-'
                print(e)
            data[-1].append(metric_value)

    context = {
        'metrics': metrics,
        'metric_names': [metric.get_name() for metric in metrics],
        'instruments': instruments,
        'instrument_names': ['%s - %s' % (instrument.name, instrument.market.name) for instrument in instruments],
        'data': data
    }
    return HttpResponse(template.render(context, request))

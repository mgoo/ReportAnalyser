from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template import loader
import os.path

from info_extractor.lib.html_extractor import read_htmlfile
from info_extractor.lib.stock_price_extractor import csv_exists, extract_csv
from info_extractor.models import Instrument, ReportAnalysis

def home(request, instrument_id):
    instrument = get_object_or_404(Instrument, id=instrument_id)
    template = loader.get_template('info_extractor/viewer/home.html')

    # Data for graphs
    stock_price = []
    stock_volume = []

    if csv_exists('stock_prices', instrument.name):
        stock_data_frame = extract_csv('stock_prices', instrument.name)

        stock_price = stock_data_frame[['Date', 'Open']].values.tolist()
        stock_price = [['Date', 'Open']] + stock_price

        stock_volume = stock_data_frame[['Date', 'Volume']].values.tolist()
        stock_volume = [['Date', 'Volume']] + stock_volume

    report_polarity = list(map(
        lambda report_analysis: [repr(report_analysis.year), report_analysis.polarity],
        ReportAnalysis.objects.filter(instrument_id=instrument.id).order_by('year')
    ))
    report_polarity = [['Year', 'Polarity']] + report_polarity

    context = {
        'instrument': instrument,
        'stock_price': stock_price,
        'stock_volume': stock_volume,
        'report_polarity': report_polarity
    }
    return HttpResponse(template.render(context, request))


def reports(request, instrument_id):
    report_list = ReportAnalysis.objects.filter(instrument_id=instrument_id)
    instrument = get_object_or_404(Instrument, id=instrument_id)
    template = loader.get_template('info_extractor/viewer/report_list.html')
    context = {'instrument': instrument, 'reports':report_list}
    return HttpResponse(template.render(context, request))


def report(request, instrument_id, report_id):
    instrument = get_object_or_404(Instrument, id=instrument_id)
    report = get_object_or_404(ReportAnalysis, id=report_id)
    filename = "report_%s" % report.year

    report_html = read_htmlfile("report_%s_formatted-html" % (report.year), instrument.name, report.year)

    template = loader.get_template('info_extractor/viewer/report.html')
    context = {
        'instrument': instrument,
        'report': report,
        'filename': filename,
        'report_html': report_html
    }
    return HttpResponse(template.render(context, request))


def tables(request, instrument_id):
    instrument = get_object_or_404(Instrument, id=instrument_id)
    template = loader.get_template('info_extractor/viewer/tables.html')
    return HttpResponse(template.render({'instrument': instrument}, request))


def stock(request, instrument_id):
    instrument = get_object_or_404(Instrument, id=instrument_id)
    template = loader.get_template('info_extractor/viewer/stock.html')
    return HttpResponse(template.render({'instrument': instrument}, request))
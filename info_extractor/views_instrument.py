from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from info_extractor.lib.html_extractor import read_htmlfile
from info_extractor.lib.stock_price_extractor import csv_exists, extract_csv, save_csv_file

from info_extractor.lib.html_extractor import save_pdf_file, pdf_to_htmlfile, html_to_text
from info_extractor.lib.text_analyser import semantic_analysis
from info_extractor.models import Instrument, ReportAnalysis


def home(request, instrument_id):
    instrument = get_object_or_404(Instrument, id=instrument_id)
    template = loader.get_template('info_extractor/instrument/home.html')

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


def report_upload(request, instrument_id):
    instrument = get_object_or_404(Instrument, id=instrument_id)
    template = loader.get_template('info_extractor/instrument/report_upload.html')
    return HttpResponse(template.render({'instrument': instrument}, request))


def report_process(request, instrument_id):
    year = request.POST['year']
    instrument = get_object_or_404(Instrument, id = instrument_id)

    save_pdf_file(request.FILES['report'], "report_%s" % year, instrument.name)

    pdf_to_htmlfile("report_%s" % year, instrument.name, year)

    report_text = html_to_text("report_%s" % year, instrument.name, year)
    polarity = semantic_analysis(report_text)

    report_analysis = ReportAnalysis(instrument_id=instrument.id, year=year, polarity=polarity)
    report_analysis.save()

    return HttpResponseRedirect(reverse('info_extractor:report_upload', args=(instrument.id, )))


def stock_upload(request, instrument_id):
    instrument = get_object_or_404(Instrument, id=instrument_id)
    template = loader.get_template('info_extractor/instrument/stock_upload.html')
    return HttpResponse(template.render({'instrument': instrument}, request))


def stock_process(request, instrument_id):
    instrument  = get_object_or_404(Instrument, id = instrument_id)

    save_csv_file(request.FILES['stock_file'], 'stock_prices', instrument.name)

    return HttpResponseRedirect(reverse('info_extractor:instrument', args=(instrument.id, )))


def instrument_list(request):
    template = loader.get_template('info_extractor/instrument/list.html')
    instruments = Instrument.objects.all()
    return HttpResponse(template.render({'instruments': instruments}, request))


def instrument_add(request):
    template = loader.get_template('info_extractor/instrument/add.html')
    return HttpResponse(template.render({}, request))


def instrument_process(request):
    instrument_obj = Instrument(name=request.POST.get('name'), market=request.POST.get('market'))
    instrument_obj.save()
    return HttpResponseRedirect(reverse('info_extractor:instrument', args=(instrument_obj.id, )))


def reports(request, instrument_id):
    report_list = ReportAnalysis.objects.filter(instrument_id=instrument_id)
    instrument = get_object_or_404(Instrument, id=instrument_id)
    template = loader.get_template('info_extractor/instrument/report_list.html')
    context = {'instrument': instrument, 'reports':report_list}
    return HttpResponse(template.render(context, request))


def report(request, instrument_id, report_id):
    instrument = get_object_or_404(Instrument, id=instrument_id)
    report = get_object_or_404(ReportAnalysis, id=report_id)

    filename = "report_%s" % report.year

    report_html = read_htmlfile("report_%s_formatted-html" % report.year, instrument.name, report.year)

    template = loader.get_template('info_extractor/instrument/report.html')
    context = {
        'instrument': instrument,
        'report': report,
        'filename': filename,
        'report_html': report_html
    }
    return HttpResponse(template.render(context, request))


def tables(request, instrument_id):
    instrument = get_object_or_404(Instrument, id=instrument_id)
    template = loader.get_template('info_extractor/instrument/tables.html')

    reports = ReportAnalysis.objects.filter(instrument_id=instrument.id).order_by('-year')
    tables = list(map(
        lambda report: {'year': report.year, 'html': read_htmlfile('report_%s_tables' % report.year, instrument.name, report.year)},
        reports
    ))
    context = {
        'instrument': instrument,
        'tables': tables
    }
    return HttpResponse(template.render(context, request))


def stock(request, instrument_id):
    instrument = get_object_or_404(Instrument, id=instrument_id)
    template = loader.get_template('info_extractor/instrument/stock.html')
    return HttpResponse(template.render({'instrument': instrument}, request))
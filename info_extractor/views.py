from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from info_extractor.lib.html_extractor import save_pdf_file, pdf_to_htmlfile, html_to_text
from info_extractor.lib.stock_price_extractor import save_csv_file
from info_extractor.lib.text_analyser import semantic_analysis
from info_extractor.models import Instrument, ReportAnalysis

def home(request):
    template = loader.get_template('info_extractor/home.html')
    return HttpResponse(template.render({}, request))


def report_upload(request, instrument_id):
    instrument = get_object_or_404(Instrument, id=instrument_id)
    template = loader.get_template('info_extractor/viewer/report_upload.html')
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
    template = loader.get_template('info_extractor/viewer/stock_upload.html')
    return HttpResponse(template.render({'instrument': instrument}, request))


def stock_process(request, instrument_id):
    instrument  = get_object_or_404(Instrument, id = instrument_id)

    save_csv_file(request.FILES['stock_file'], 'stock_prices', instrument.name)

    return HttpResponseRedirect(reverse('info_extractor:instrument', args=(instrument.id, )))


def instrument_list(request):
    instruments = Instrument.objects.all()
    return render(request, 'info_extractor/instrument_list.html', {'instruments': instruments})


def instrument_add(request):
    template = loader.get_template('info_extractor/instrument_add.html')
    return HttpResponse(template.render({}, request))


def instrument_process(request):
    instrument_obj = Instrument(name=request.POST.get('name'), market=request.POST.get('market'))
    instrument_obj.save()
    return HttpResponseRedirect(reverse('info_extractor:instrument', args=(instrument_obj.id, )))





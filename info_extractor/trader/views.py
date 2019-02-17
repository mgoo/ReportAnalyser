from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader


def list(request):
    template = loader.get_template('info_extractor/trader_list.html')
    return HttpResponse(template.render({}, request))
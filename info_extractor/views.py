from django.http import HttpResponse
from django.template import loader


def home(request):
    template = loader.get_template('info_extractor/home.html')
    return HttpResponse(template.render({}, request))



from django.http import HttpResponse
from django.template import Context, loader
from factopy.models import Process

# Create your views here.


def index(request):
    program_list = Process.objects.all()
    template = loader.get_template('factopy/index.html')
    context = Context({
        'program_list': program_list,
    })
    return HttpResponse(template.render(context))

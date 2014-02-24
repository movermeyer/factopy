from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render, redirect
from factopy.models import ComplexProcess, Importer

# Create your views here.

def index(request):
	program_list = ComplexProcess.objects.all()
	template = loader.get_template('factopy/index.html')
	context = Context({
		'program_list': program_list,
	})
	return HttpResponse(template.render(context))

def execute(request, program_id):
	programs = ComplexProcess.objects.filter(id=program_id)
	programs[0].execute()
	return redirect('/factopy/status')

def status(request):
	programs = ComplexProcess.objects.all()
	return render(request, 'factopy/status.html', {'programs': programs})

def update(request):
	new_importers = len(Importer.setup_unloaded())
	template = loader.get_template('factopy/update.html')
	context = Context({
		'new_importers': new_importers,
	})
	return HttpResponse(template.render(context))

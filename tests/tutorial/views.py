import adjax

def hello_world(request):
    adjax.replace(request, 'h1', 'Hello world')
    return adjax.response(request)

from django.shortcuts import render_to_response
from django.template.context import RequestContext

def index(request):
    return render_to_response('tutorial/index.html', context_instance=RequestContext(request))


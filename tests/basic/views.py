
""" Adjax testing views.

    The following views make use of the adjax library, allowing them to be tested.
"""

import adjax

@adjax.adjax_response
def replace(request):
    """ Replace an HTML element """
    adjax.replace(request, '#abc', 'Hello world')
   
@adjax.adjax_response
def hide(request):
    """ Hide an HTML element """
    adjax.hide(request, '#xyz')

@adjax.adjax_response
def messages(request):
    """ Display some messages """
    adjax.success(request, "This is your first success")
    adjax.info(request, "This is your first info")
    adjax.warning(request, "This is your first warning")
    adjax.error(request, "This is your first error")
    adjax.debug(request, "This is your first debug")
   
@adjax.adjax_response
def update(request):
    """ Update a django object """
    my_obj = MyModel(name="Abc", color="blue", price=123)
    adjax.update(request, my_obj, ('name', 'color'))

from django import forms
from basic.models import MyModel
class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
   
@adjax.adjax_response
def forms(request):
    """ Display form validation errors. """
    if request.method == "POST":
        my_form = MyForm(request.POST, prefix="withprefix")
        if my_form.is_valid():
            adjax.redirect(request, 'do_nothing')
    else:
        my_form = MyForm({'name': "Blah", 'price': "123"}, prefix="withprefix") # color missing!
    adjax.form(request, my_form)
   
@adjax.adjax_response
def redirect(request):
    """ Redirect the browser (using javascript). """
    adjax.redirect(request, 'do_nothing')
   
@adjax.adjax_response
def django_redirect(request):
    """ This makes use of the standard django redirect function. """
    from django.shortcuts import redirect
    return redirect('do_nothing')

@adjax.adjax_response
def extra(request):
    """ Add information to the json response """
    return {'one': 123}

@adjax.adjax_response
def extra_2(request):
    """ Add extra information to the ajax response explicitly """
    adjax.extra(request, 'two', 234)
    return {'one': 123}

@adjax.adjax_response
def template_include_update(request):
    """ Replace rendered content with the output of a template. """
    adjax.render_to_response(request, 'basic/_included.html', {'abc': 'xyz123'})
    adjax.render_to_response(request, 'basic/_included.html', {'abc': 'mno456'}, prefix="tree")

def template_include_tag(request):
    """ Render a template that uses the template include tag. """
    from django.shortcuts import render_to_response
    return render_to_response('basic/template_includer.html', {'abc': '13579'})

@adjax.adjax_response
def do_everything(request):
    """ Putting everything together. """
    adjax.replace(request, '#abc', 'Hello world')
    adjax.hide(request, '#xyz')
    adjax.success(request, "This is your first success")
    adjax.info(request, "This is your first info")
    adjax.warning(request, "This is your first warning")
    adjax.error(request, "This is your first error")
    adjax.debug(request, "This is your first debug")
    my_obj = MyModel(name="Abc", color="blue", price=123)
    adjax.update(request, my_obj, ('name', 'color'))
    my_form = MyForm({'name': "ABC", 'price': 123}, prefix="withprefix")
    adjax.form(request, my_form)
    adjax.redirect(request, 'do_nothing')
    adjax.extra(request, 'two', 234)
    adjax.render_to_response(request, 'basic/_included.html', {'abc': 'xyz123'})
    adjax.render_to_response(request, 'basic/_included.html', {'abc': 'mno456'}, prefix="tree")
    return {'one': 123}

def do_nothing(request):
    """ A view that can't go wrong! 
        This is a good target for testing redirects.
    """
    from django.http import HttpResponse
    return HttpResponse()

def demo(request):
    """ This view provides a demonstration page for Adjax.
    """
    context = {}
    context['form'] = MyForm(prefix="withprefix")
    context['my_obj'] = MyModel(name="Tree", color="green", price=899)
    context['abc'] = "123 waiting 456"
    from django.shortcuts import render_to_response
    from django.template.context import RequestContext
    return render_to_response('basic/demo.html', context, context_instance=RequestContext(request))

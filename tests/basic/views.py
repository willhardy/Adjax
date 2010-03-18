
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
    my_obj = MyModel.objects.create(name="Abc", color="blue", price=123)
    adjax.update(request, my_obj, ('name', 'color'))

from django import forms
from basic.models import MyModel
class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
   
@adjax.adjax_response
def forms(request):
    """ Display form validation errors. """
    my_form = MyForm({'name': "Blah", 'price': "123"}) # color missing!
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
def do_everything(request):
    """ Putting everything together. """
    adjax.replace(request, '#abc', 'Hello world')
    adjax.hide(request, '#xyz')
    adjax.success(request, "This is your first success")
    adjax.info(request, "This is your first info")
    adjax.warning(request, "This is your first warning")
    adjax.error(request, "This is your first error")
    adjax.debug(request, "This is your first debug")
    my_obj = MyModel.objects.create(name="Abc", color="blue", price=123)
    adjax.update(request, my_obj, ('name', 'color'))
    my_form = MyForm({'name': "ABC", 'price': 123})
    adjax.form(request, my_form)
    adjax.redirect(request, 'do_nothing')
    adjax.extra(request, 'two', 234)
    return {'one': 123}

def do_nothing(request):
    """ A view that can't go wrong! 
        This is a good target for testing redirects.
    """
    from django.http import HttpResponse
    return HttpResponse()

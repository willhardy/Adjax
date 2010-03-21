"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.utils import simplejson

from adjax.utils import get_key
from basic.models import MyModel

class BasicTests(TestCase):
    def get_view(self, name):
        self.client = Client()
        response = self.client.get(reverse(name), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        return  simplejson.loads(response.content)

    def assert_value_in(self, container, value, *keys):
        for key in keys:
            try:
                container = container[key]
            except (IndexError, KeyError):
                self.fail('"%s" missing from container: %s' % (key, repr(container)))
        self.assertEqual(container, value)

    def test_replace(self):
        self.assert_value_in(self.get_view('replace'), 'Hello world', 'replace', '#abc')

    def test_hide(self):
        self.assert_value_in(self.get_view('hide'), '#xyz', 'hide', 0)

    def test_messages(self):
        data = self.get_view('messages')
        assert 'messages' in data, repr(data)
        for message in data['messages']:
            assert message['content'].startswith(u"This is your first "), message
            assert message['content'].endswith(message['tags']), message

    def test_update(self):
        data = self.get_view('update')
        assert 'update' in data, repr(data)
        model = MyModel(name="Abc", color="blue")
        name_key = get_key(model, 'name')
        color_key = get_key(model, 'color')
        price_key = get_key(model, 'price')
        update_dict = data['update']
        assert price_key not in update_dict
        try:
            self.assertEqual(update_dict[name_key], "Abc")
            self.assertEqual(update_dict[color_key], "blue")
        except KeyError:
            self.fail(repr(update_dict))

    def test_forms(self):
        data = self.get_view('forms')
        assert 'forms' in data, repr(data)
        assert 'id_withprefix-color' in data['forms'], repr(data)
        self.assertEqual(data['forms']['id_withprefix-color'][0], u"This field is required.")

    def test_redirect(self):
        data = self.get_view('redirect')
        assert 'redirect' in data, repr(data)
        self.assertEqual(data['redirect'], reverse('do_nothing'))

    def test_django_redirect(self):
        data = self.get_view('django_redirect')
        assert 'redirect' in data, repr(data)
        self.assertEqual(data['redirect'], reverse('do_nothing'))

    def test_extra(self):
        data = self.get_view('extra')
        assert 'extra' in data, repr(data)
        assert 'one' in data['extra'], repr(data['extra'])
        self.assertEqual(data['extra']['one'], 123)

    def test_extra_2(self):
        data = self.get_view('extra_2')
        assert 'extra' in data, repr(data)
        assert 'one' in data['extra'], repr(data['extra'])
        self.assertEqual(data['extra']['one'], 123)
        assert 'two' in data['extra'], repr(data['extra'])
        self.assertEqual(data['extra']['two'], 234)


    def test_do_everything(self):
        data = self.get_view('do_everything')
        assert 'replace' in data, repr(data)
        assert 'hide' in data, repr(data)
        assert 'messages' in data, repr(data)
        assert 'update' in data, repr(data)
        assert 'forms' in data, repr(data)
        assert 'redirect' in data, repr(data)
        assert 'extra' in data, repr(data)

        # replace
        self.assert_value_in(data, 'Hello world', 'replace', '#abc')
        # hide
        self.assert_value_in(data, '#xyz', 'hide', 0)
        # messages
        for message in data['messages']:
            assert message['content'].startswith(u"This is your first "), message
            assert message['content'].endswith(message['tags']), message
        # update
        model = MyModel(name="Abc", color="blue")
        name_key = get_key(model, 'name')
        color_key = get_key(model, 'color')
        price_key = get_key(model, 'price')
        update_dict = data['update']
        assert price_key not in update_dict
        try:
            self.assertEqual(update_dict[name_key], "Abc")
            self.assertEqual(update_dict[color_key], "blue")
        except KeyError:
            self.fail(repr(update_dict))
        # forms
        assert 'id_withprefix-color' in data['forms'], repr(data)
        self.assertEqual(data['forms']['id_withprefix-color'][0], u"This field is required.")
        # redirect
        self.assertEqual(data['redirect'], reverse('do_nothing'))
        # extra
        self.assertEqual(data['extra']['one'], 123)
        self.assertEqual(data['extra']['two'], 234)

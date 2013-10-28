# -*- coding: utf-8 -*-
import sys
from .inputs import String
from .inputs import Integer
from .inputs import Select
from .inputs import Boolean
from .inputs import MultiSelect
from .inputs import Branch
from .utils import numeric_options
from .utils import prepare_stylesheet


class AddAction(object):

    def __init__(self, form):
        self.form = form

    def __call__(self, key, obj):
        self.form._fields.append((key, obj))

    def string(self, key, label, **kwargs):
        obj = String(label, **kwargs)
        self.form._add(key, obj)
        return self.form

    def int(self, key, label, **kwargs):
        obj = Integer(label, **kwargs)
        self.form._add(key, obj)
        return self.form

    def select(self, key, label, choices, option_format=numeric_options, **kwargs):
        obj = Select(label, choices, option_format, **kwargs)
        self.form._add(key, obj)
        return self.form

    def multiselect(self, key, label, choices, done_label='Done', option_format=numeric_options, **kwargs):
        obj = MultiSelect(label, choices, done_label, option_format, **kwargs)
        self.form._add(key, obj)
        return self.form

    def bool(self, key, label, **kwargs):
        obj = Boolean(label, **kwargs)
        self.form._add(key, obj)
        return self.form

    def branch(self, handler, *args, **kwargs):
        obj = Branch(handler, *args, **kwargs)
        self.form._add(id(obj), obj)
        return self.form


class Form(object):

    @property
    def add(self):
        action = AddAction(self)
        return action

    def __init__(self):
        self._fields = []

    def _add(self, key, obj):
        self._fields.append((key, obj))

    def run(self, prefix=None, stylesheet=None):
        styles = None

        styles = prepare_stylesheet(stylesheet)

        prefix = '' if prefix is None else prefix
        for label, input in iter(self._fields):
            input(form=self, prefix=prefix, stylesheet=styles)

    def __len__(self):
        return len(self._fields)

    def __iter__(self):
        for k, v in iter(self._fields):
            if not isinstance(v, Branch):
                yield k, v.value

    def __getattr__(self, key):
        try:
            # we were using an ordereddict so access was pretty close to
            # O(1), switched to lists in order to facilitate branching
            # this lookup will be O(N)
            return next(x[1] for x in self._fields if x[0] == key)
        except StopIteration:
            raise AttributeError

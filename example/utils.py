# -*- coding: utf-8 -*-

from dolmen.forms.base import Fields


def extract_object_fields(obj, *ifaces):
    fields = Fields()
    for iface in ifaces:
        if iface.providedBy(obj):
            fields += Fields(iface)
    return fields
    

class StateFields(object):

    def __init__(self, *conditions):
        self.key = '_statefields'
        self.conditions = conditions

    def __get__(self, form, type=None):
        if form is None:
            return Fields()
        
        content = form.getContentData().getContent()
        cache = form.__dict__.get(self.key, None)
        if cache is None:
            form.__dict__[self.key] = cache = extract_object_fields(
                content, *self.conditions)
        return cache

    def __set__(self, form, value):
        raise AttributeError

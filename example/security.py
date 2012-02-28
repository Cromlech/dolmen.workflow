# -*- coding: utf-8 -*-

import grokcore.security as grok
from zope.interface import moduleProvides


class TriggerWorkflow(grok.Permission):
    grok.name('ditrimag.TriggerWorkflow')

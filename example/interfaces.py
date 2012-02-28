# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute
from dolmen.workflow import IWorkflowState
from zeam.form.base.interfaces import IComponent


class ITransitionNotification(Interface):
    pass


class IStateComponent(IWorkflowState, IComponent):
    pass

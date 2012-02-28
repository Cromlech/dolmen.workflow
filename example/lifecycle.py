# -*- coding: utf-8 -*-

import grok
from some_hypothetical_package import ITask
from dolmen.forms.base import utils
from dolmen.workflow import Error, IObjectStateChanged, IStatesManager
from zope.interface import implements, moduleProvides
from zope.publisher.interfaces.browser import IBrowserRequest


class StateChanged(object):
    implements(IObjectStateChanged)

    def __init__(self, object, principal, old_state, new_state, transition):
        self.object = object
        self.new_state = new_state
        self.old_state = old_state
        self.transition = transition
        self.principal = principal


class TaskManager(grok.MultiAdapter):
    grok.adapts(ITask, IBrowserRequest)
    grok.provides(IStatesManager)
    implements(IStatesManager)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @apply
    def current_state():

        def fget(self):
            return self.context.state

        def fset(self, new_state):
            grok.notify(
                StateChanged(
                    self.context,
                    principal=self.request.principal,
                    old_state=self.context.state,
                    new_state=new_state,
                    transition=new_state.action))

            utils.notify_changes(self.context, {ITask: ['state']})
            self.context.state = new_state
        return property(fget, fset)

    @property
    def available_states(self):
        return self.context.state.get_reachable_states(self.context)

    def set_state(self, state_id):
        errors = self.current_state.check_locks(self.context)
        if not errors:
            try:
                target = self.current_state.states.get(state_id)
            except KeyError:
                return [Error(title="Unknown State")]
            if target is not None:
                errors = target.check_constraints(self.context)
                if not errors:
                    self.current_state = target
        return errors

    def trigger_transition(self, action):
        target = self.available_states.get(action)
        if target is None:
            return [Error(title="Unknown action")]
        self.current_state = target

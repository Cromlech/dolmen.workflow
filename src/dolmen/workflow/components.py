# -*- coding: utf-8 -*-

from dolmen.workflow import IWorkflowState, IValidator, IError
from dolmen.collection.components import Component, Collection
from zope.interface import implements


class Error(Component):
    """A non-exception error component.
    """
    implements(IError)
    

class ValidationError(Exception):
    pass


class States(Collection):
    type = IWorkflowState


class Validators(Collection):
    type = IValidator


def check_validators(item, validators, raiseErrors=False):
    if validators is None:
        return None

    if raiseErrors is False:
        errors = []
    else:
        errors = None

    for validator in validators:
        error = validator.validate(item)
        if error is not None:
            assert IError.providedBy(error)
            if errors is None:
                raise ValidationError(error.title)
            else:
                errors.append(error)
    return errors


class State(Component):
    """A persistent implementation of a Workflow State.
    """
    implements(IWorkflowState)

    def __init__(self, title=None, identifier=None, description=None,
                 action=None, pre_validators=None, post_validators=None,
                 states=None):
        super(State, self).__init__(title, identifier)
        self.description = description
        self.action = action
        self.states = states or States()
        self.pre_validators = pre_validators or Validators()
        self.post_validators = post_validators or Validators()

    def check_constraints(self, item, raiseErrors=False):
        return check_validators(item, self.pre_validators)

    def check_locks(self, item, raiseErrors=False):
        return check_validators(item, self.post_validators)

    def get_reachable_states(self, item):
        if bool(self.check_locks(item)) is False:
            return dict([(state.action or state.title, state)
                         for state in self.states
                         if not state.check_constraints(item)])
        return {}

# -*- coding: utf-8 -*-

from dolmen.collection.interfaces import IComponent, ICollection
from zope.component.interfaces import IObjectEvent
from zope.interface import Interface, Attribute
from zope.schema import Object


class IError(Interface):
    """A workflow-related error.
    """


class IValidator(Interface):
    """A simple validator.
    """
    description = Attribute("Detailed description of the validator.")

    def validate(obj):
        """Return an IError or None.
        """


class IWorkflowState(IComponent):
    """Workflow State
    Nomenclature::
       * constraints: pre-validation
       * locks: post-validation
    """
    description = Attribute(u"Detailed description of the state.")

    pre_validators = Object(
        title=u"State constraints",
        description=u"Locks that forbid the item to reach this state.",
        schema=ICollection,
        required=False)

    post_validators = Object(
        title=u"State locks",
        description=u"Locks that forbid the item to be changed from state.",
        schema=ICollection,
        required=False)

    states = Object(
        title=u"Reachable states",
        description=u"Other states that can be reached from this state.",
        schema=ICollection)

    def check_constraints(item, raiseErrors=False):
        """Checks the constraints against the given object.
        If the raiseErrors flag is set to True, an error is risen
        if any errors is encountered.
        """

    def check_locks(item, raiseErrors=False):
        """Checks the locks against the given object.
        If the raiseErrors flag is set to True, an error is risen
        if any errors is encountered.
        """

    def get_reachable_states(item):
        """Returns a collection of states that are currently reachable.
        """


class IStatesManager(Interface):
    """Stateful treatment processor.
    """
    current_state = Object(
        title=u"Current state",
        required=True,
        schema=IWorkflowState)

    available_states = Object(
        title=u"Reachable states",
        description=u"Other states that can be reached from this state.",
        schema=ICollection,
        required=False,
        default=None)

    def set_state(state_id):
        """Sets the current state. Returns a list of errors or None.
        """

    def trigger_transition(action):
        """Sets the current state according to the given action.
        """


class IObjectStateChanged(IObjectEvent):
    principal = Attribute("Person who trigged the change.")
    old_state = Attribute("The state before the transition.")
    new_state = Attribute("The state after the transition.")
    transition = Attribute("The transition used in the state change.")
